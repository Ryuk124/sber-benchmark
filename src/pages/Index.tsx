import { useState } from "react";
import { BarChart3, Download, History, Settings, AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { BankSelector, Bank } from "@/components/BankSelector";
import { ProductSelector } from "@/components/ProductSelector";
import { CriteriaSelector, Criterion } from "@/components/CriteriaSelector";
import { ComparisonTable } from "@/components/ComparisonTable";
import { AIInsights } from "@/components/AIInsights";
import { GrafanaPlaceholder } from "@/components/GrafanaPlaceholder";
import { useToast } from "@/hooks/use-toast";
import { useComparisonData } from "@/hooks/use-comparison-data";

const Index = () => {
  const { toast } = useToast();
  const [selectedBanks, setSelectedBanks] = useState<Bank[]>([
    { id: "sber", name: "Сбербанк" },
  ]);
  const [selectedProduct, setSelectedProduct] = useState<string>("deposits");
  const [selectedCriteria, setSelectedCriteria] = useState<Criterion[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  // Fetch comparison data from API
  const {
    data: comparisonData,
    sources,
    loading: dataLoading,
    error: dataError,
    isMock,
    lastFetchTime,
    confidence,
    refetch,
  } = useComparisonData(selectedBanks, selectedCriteria, selectedProduct, {
    enabled: showResults,
  });

  const handleGenerate = async () => {
    if (selectedBanks.length < 2) {
      toast({
        title: "Недостаточно банков",
        description: "Выберите минимум 2 банка для сравнения",
        variant: "destructive",
      });
      return;
    }

    if (!selectedProduct) {
      toast({
        title: "Продукт не выбран",
        description: "Выберите продукт для анализа",
        variant: "destructive",
      });
      return;
    }

    if (selectedCriteria.length === 0) {
      toast({
        title: "Критерии не выбраны",
        description: "Выберите минимум 1 критерий для сравнения",
        variant: "destructive",
      });
      return;
    }

    setIsGenerating(true);
    setShowResults(true);
    
    // Simulate UI processing
    await new Promise((resolve) => setTimeout(resolve, 500));
    
    setIsGenerating(false);
    
    toast({
      title: "Отчёт загружен",
      description: `Сгенерирован отчёт по ${selectedBanks.length} банкам и ${selectedCriteria.length} критериям`,
    });
  };

  const handleExport = () => {
    toast({
      title: "Экспорт запущен",
      description: "Отчёт будет загружен в формате PDF",
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src="/logo.png?v=2" alt="BankBench AI Logo" className="h-10 w-10 rounded-lg" />
              <div>
                <h1 className="text-2xl font-bold text-foreground">BankBench AI</h1>
                <p className="text-sm text-muted-foreground">
                  Интеллектуальный бенчмаркинг банковских продуктов
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                <History className="w-4 h-4 mr-2" />
                История
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                Настройки
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Parameters Panel */}
        <Card className="p-6 bg-gradient-to-br from-card to-muted/20">
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-1">
                Параметры анализа
              </h2>
              <p className="text-sm text-muted-foreground">
                Настройте параметры для сравнительного анализа банковских продуктов
              </p>
            </div>

            <Separator />

            <div className="grid gap-6 md:grid-cols-2">
              <div className="space-y-6">
                <BankSelector
                  selectedBanks={selectedBanks}
                  onChange={setSelectedBanks}
                />
                <ProductSelector
                  selectedProduct={selectedProduct}
                  onChange={setSelectedProduct}
                />
              </div>

              <CriteriaSelector
                selectedCriteria={selectedCriteria}
                onChange={setSelectedCriteria}
              />
            </div>

            <Separator />

            <div className="flex justify-end">
              <Button
                onClick={handleGenerate}
                disabled={isGenerating}
                size="lg"
                className="bg-gradient-primary hover:opacity-90 text-primary-foreground font-semibold px-8"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin mr-2" />
                    Генерация отчёта...
                  </>
                ) : (
                  <>
                    <BarChart3 className="w-5 h-5 mr-2" />
                    Сгенерировать отчёт
                  </>
                )}
              </Button>
            </div>
          </div>
        </Card>

        {/* Results Section */}
        {showResults && (
          <div className="space-y-8">
            {/* Data Status Bar */}
            <Card className={`p-4 ${isMock ? "bg-yellow-50 border-yellow-200" : "bg-green-50 border-green-200"}`}>
              <div className="flex items-start gap-3">
                <AlertCircle className={`w-5 h-5 mt-0.5 flex-shrink-0 ${isMock ? "text-yellow-600" : "text-green-600"}`} />
                <div className="flex-1 space-y-1">
                  <p className={`text-sm font-medium ${isMock ? "text-yellow-900" : "text-green-900"}`}>
                    {isMock ? "Демо-данные" : "Реальные данные"}
                  </p>
                  <p className={`text-xs ${isMock ? "text-yellow-700" : "text-green-700"}`}>
                    {isMock 
                      ? "Данные сгенерированы локально для демонстрации"
                      : `Данные актуальны на ${lastFetchTime ? new Date(lastFetchTime).toLocaleString("ru-RU") : "неизвестное время"}`
                    }
                  </p>
                  {dataError && (
                    <p className="text-xs text-red-700 mt-2">
                      ⚠️ Ошибка при загрузке данных: {dataError}
                    </p>
                  )}
                </div>
                <Button
                  onClick={() => refetch()}
                  disabled={dataLoading}
                  variant="ghost"
                  size="sm"
                  className="flex-shrink-0"
                >
                  <RefreshCw className={`w-4 h-4 ${dataLoading ? "animate-spin" : ""}`} />
                </Button>
              </div>
            </Card>

            {/* Table Section */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-foreground">
                  Сравнительная таблица
                </h2>
                <div className="flex gap-2">
                  {sources.length > 0 && (
                    <div className="flex gap-1">
                      {sources.map((source, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {source.name}
                        </Badge>
                      ))}
                    </div>
                  )}
                  <Button
                    onClick={handleExport}
                    variant="outline"
                    size="sm"
                    className="border-primary/30 text-primary hover:bg-primary/10"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Экспортировать
                  </Button>
                </div>
              </div>

              {dataLoading ? (
                <Card className="p-8 text-center">
                  <div className="flex flex-col items-center gap-3">
                    <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                    <p className="text-muted-foreground">Загрузка данных...</p>
                  </div>
                </Card>
              ) : (
                <ComparisonTable
                  banks={selectedBanks}
                  criteria={selectedCriteria}
                  data={comparisonData}
                />
              )}
            </div>

            {/* AI Insights */}
            {!dataLoading && (
              <AIInsights 
                banks={selectedBanks}
                criteria={selectedCriteria}
                product={selectedProduct}
              />
            )}

            {/* Grafana Integration Placeholder */}
            <GrafanaPlaceholder className="animate-fade-in" />
          </div>
        )}

        {!showResults && (
          <Card className="p-12 text-center border-dashed border-2">
            <div className="max-w-md mx-auto space-y-4">
              <div className="w-16 h-16 rounded-full bg-muted/50 flex items-center justify-center mx-auto">
                <BarChart3 className="w-8 h-8 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">
                Готовы к анализу?
              </h3>
              <p className="text-sm text-muted-foreground">
                Настройте параметры выше и нажмите &quot;Сгенерировать отчёт&quot; для
                получения детального сравнительного анализа
              </p>
            </div>
          </Card>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
            <p>© 2025 BankBench AI. Система бенчмаркинга для Сбербанка</p>
            <div className="flex gap-4">
              <a href="#" className="hover:text-foreground transition-colors">
                Документация
              </a>
              <a href="#" className="hover:text-foreground transition-colors">
                API
              </a>
              <a href="#" className="hover:text-foreground transition-colors">
                Поддержка
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
