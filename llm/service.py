import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from llm.llm_qwen import analyze_with_llm
from dotenv import load_dotenv
from typing import List, Dict, Optional

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
            self.conn.commit()

    def analyze_and_store(
        self,
        pages: List[Dict],
        llm_model="Qwen-14B",
        prompt_version="v1",
        time_override: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Берём список страниц (от парсера), прогоняем через LLM, сохраняем результаты в БД.
        Если time_override задан, он сохранится в поле 'time', иначе = parsed_at.
        """
        results = []
        for page in pages:
            if page.get("cleaned_text"):
                analysis = analyze_with_llm(
                    text=page["cleaned_text"],
                    competitor=page["competitor"],
                    product=page["product"],
                    criterion=page["criterion"]
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

    def query(
        self,
        competitor: Optional[str] = None,
        product: Optional[str] = None,
        criterion: Optional[str] = None
    ) -> List[Dict]:
        """
        Получить записи из БД с фильтрами
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