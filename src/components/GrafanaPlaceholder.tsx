import { BarChart3, ExternalLink, Settings, RefreshCw, TrendingUp, Users, DollarSign } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { useState } from "react";

interface GrafanaPlaceholderProps {
  className?: string;
  dashboardUrl?: string;
  showDemo?: boolean;
}

export const GrafanaPlaceholder = ({ 
  className = "", 
  dashboardUrl = "http://localhost:3000/d/cd1186af-ff09-478c-b382-c61e98101210/bank-comparison?theme=dark&kiosk=tv",
  showDemo = true 
}: GrafanaPlaceholderProps) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleIframeLoad = () => {
    setIsLoading(false);
    setError(null);
  };

  const handleIframeError = () => {
    setError("Не удалось загрузить Grafana дашборд. Убедитесь, что Grafana запущена на localhost:3000");
    setIsLoading(false);
  };

  const openGrafanaInNewTab = () => {
    window.open(dashboardUrl, "_blank");
  };

  if (!showDemo) {
    return (
      <Card className={`border-dashed border-2 border-secondary/30 ${className}`}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-secondary/10">
                <BarChart3 className="w-6 h-6 text-secondary" />
              </div>
              <div>
                <CardTitle className="text-lg">Grafana Дашборды</CardTitle>
                <CardDescription>Продвинутая визуализация и аналитика</CardDescription>
              </div>
            </div>
            <Badge variant="outline" className="border-secondary/30 text-secondary">
              Demo режим отключен
            </Badge>
          </div>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      <Card className="border-secondary/30">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-secondary/10">
                <BarChart3 className="w-6 h-6 text-secondary" />
              </div>
              <div>
                <CardTitle className="text-lg">Grafana Дашборды</CardTitle>
                <CardDescription>Визуализация данных в реальном времени</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {isLoading && <RefreshCw className="w-4 h-4 text-secondary animate-spin" />}
              <Badge variant="secondary">Подключено</Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Mock Charts instead of iframe */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Rates Trend */}
        <Card className="border-secondary/30">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-base">Тренды процентных ставок</CardTitle>
                <CardDescription>По депозитам, последние 6 месяцев</CardDescription>
              </div>
              <TrendingUp className="w-5 h-5 text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={[
                { month: "Янв", sber: 4.2, vtb: 4.5, alpha: 4.3 },
                { month: "Фев", sber: 4.3, vtb: 4.6, alpha: 4.4 },
                { month: "Мар", sber: 4.5, vtb: 4.7, alpha: 4.5 },
                { month: "Апр", sber: 4.6, vtb: 4.8, alpha: 4.6 },
                { month: "Май", sber: 4.7, vtb: 4.9, alpha: 4.7 },
                { month: "Июн", sber: 4.8, vtb: 5.0, alpha: 4.8 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))" }} />
                <Legend />
                <Line type="monotone" dataKey="sber" stroke="hsl(142 76% 36%)" strokeWidth={2} name="Сбербанк" />
                <Line type="monotone" dataKey="vtb" stroke="hsl(207 90% 54%)" strokeWidth={2} name="ВТБ" />
                <Line type="monotone" dataKey="alpha" stroke="hsl(36 100% 57%)" strokeWidth={2} name="Альфа" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Market Share */}
        <Card className="border-secondary/30">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-base">Доля рынка депозитов</CardTitle>
                <CardDescription>Текущее распределение</CardDescription>
              </div>
              <Users className="w-5 h-5 text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={[
                    { name: "Сбербанк", value: 45 },
                    { name: "ВТБ", value: 28 },
                    { name: "Альфа", value: 18 },
                    { name: "Прочие", value: 9 },
                  ]}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name} ${value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  <Cell fill="hsl(142 76% 36%)" />
                  <Cell fill="hsl(207 90% 54%)" />
                  <Cell fill="hsl(36 100% 57%)" />
                  <Cell fill="hsl(0 0% 85%)" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Product Comparison */}
        <Card className="border-secondary/30 lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-base">Сравнение предложений по типам</CardTitle>
                <CardDescription>Количество продуктов и услуг по категориям</CardDescription>
              </div>
              <DollarSign className="w-5 h-5 text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[
                { category: "Депозиты", sber: 5, vtb: 4, alpha: 6 },
                { category: "Кредиты", sber: 8, vtb: 7, alpha: 6 },
                { category: "Карты", sber: 12, vtb: 10, alpha: 11 },
                { category: "Страховка", sber: 4, vtb: 3, alpha: 2 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="category" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))" }} />
                <Legend />
                <Bar dataKey="sber" fill="hsl(142 76% 36%)" name="Сбербанк" />
                <Bar dataKey="vtb" fill="hsl(207 90% 54%)" name="ВТБ" />
                <Bar dataKey="alpha" fill="hsl(36 100% 57%)" name="Альфа" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Actions */}
      <div className="flex gap-2 justify-end">
        <Button 
          variant="outline" 
          size="sm"
          onClick={() => window.location.reload()}
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Обновить
        </Button>
        <Button 
          variant="outline" 
          size="sm"
          onClick={openGrafanaInNewTab}
        >
          <ExternalLink className="w-4 h-4 mr-2" />
          Открыть в новой вкладке
        </Button>
        <Button 
          variant="secondary" 
          size="sm"
          onClick={() => window.open("http://localhost:3000", "_blank")}
        >
          <Settings className="w-4 h-4 mr-2" />
          Grafana
        </Button>
      </div>
    </div>
  );
};
