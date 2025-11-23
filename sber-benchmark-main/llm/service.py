import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

from llm.llm_qwen import run_llm

load_dotenv()

class LLMService:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            database=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD")
        )
        self._init_db()

    def _init_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS llm_analysis (
                id SERIAL PRIMARY KEY,
                competitor TEXT NOT NULL,
                product TEXT NOT NULL,
                criterion TEXT NOT NULL,
                value TEXT,
                source_url TEXT,
                parsed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                llm_model TEXT,
                llm_prompt_version TEXT
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS llm_recommendations (
                id SERIAL PRIMARY KEY,
                analysis_id INT REFERENCES llm_analysis(id),
                recommendation_text TEXT,
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
            );
            """)
            self.conn.commit()

    def analyze_and_store(
        self,
        pages: List[Dict],
        llm_model="Qwen-14B",
        prompt_version="v1",
        time_override: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Берём список страниц (от парсера), прогоняем через LLM (facts), сохраняем результаты в БД.
        """
        results = []
        for page in pages:
            if page.get("cleaned_text"):
                analysis = run_llm(
                    competitor=page["competitor"],
                    product=page["product"],
                    criterion=page["criterion"],
                    text=page["cleaned_text"],
                    mode="facts"
                )
                parsed_at = datetime.fromisoformat(
                    page.get("parsed_at", datetime.utcnow().isoformat())
                )
                time_value = time_override if time_override else parsed_at

                record = {
                    **analysis,
                    "source_url": page.get("source_url"),
                    "parsed_at": parsed_at,
                    "time": time_value,
                    "llm_model": llm_model,
                    "llm_prompt_version": prompt_version
                }
                self._insert_record(record)
                results.append(record)
        return results

    def _insert_record(self, record: Dict):
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO llm_analysis (
                competitor, product, criterion, value, source_url,
                parsed_at, time, llm_model, llm_prompt_version
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record["competitor"],
                record["product"],
                record["criterion"],
                record["value"],
                record["source_url"],
                record["parsed_at"],
                record["time"],
                record["llm_model"],
                record["llm_prompt_version"]
            ))
        self.conn.commit()

    def generate_recommendations(self,
        competitor: Optional[str] = None,
        product: Optional[str] = None,
        criterion: Optional[str] = None
    ) -> List[Dict]:
        """
        Берёт факты из llm_analysis, прогоняет через LLM (recommendations), сохраняет в БД.
        """
        q = "SELECT * FROM llm_analysis WHERE 1=1"
        params = []
        if competitor:
            q += " AND competitor=%s"
            params.append(competitor)
        if product:
            q += " AND product=%s"
            params.append(product)
        if criterion:
            q += " AND criterion=%s"
            params.append(criterion)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(q, params)
            facts = cur.fetchall()

        recommendations = []
        for fact in facts:
            rec_text = run_llm(
                competitor=fact["competitor"],
                product=fact["product"],
                criterion=fact["criterion"],
                mode="recommendations",
                context=fact
            )
            self._insert_recommendation(fact["id"], rec_text)
            recommendations.append({
                "analysis_id": fact["id"],
                "recommendation_text": rec_text
            })
        return recommendations

    def _insert_recommendation(self, analysis_id: int, rec_text: str):
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO llm_recommendations (analysis_id, recommendation_text)
            VALUES (%s, %s)
            """, (analysis_id, rec_text))
        self.conn.commit()

    # ---- Запросы ----
    def query(self,
        competitor: Optional[str] = None,
        product: Optional[str] = None,
        criterion: Optional[str] = None
    ) -> List[Dict]:
        """
        Получить записи из llm_analysis с фильтрами
        """
        q = "SELECT * FROM llm_analysis WHERE 1=1"
        params = []
        if competitor:
            q += " AND competitor=%s"
            params.append(competitor)
        if product:
            q += " AND product=%s"
            params.append(product)
        if criterion:
            q += " AND criterion=%s"
            params.append(criterion)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(q, params)
            return cur.fetchall()

    def query_recommendations(self) -> List[Dict]:
        """
        Получить все рекомендации
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM llm_recommendations")
            return cur.fetchall()