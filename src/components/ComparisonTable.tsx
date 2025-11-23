import { Check, X, Building2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Bank } from "./BankSelector";
import type { Criterion } from "./CriteriaSelector";

interface ComparisonData {
  [bankId: string]: {
    [criterionId: string]: boolean;
  };
}

interface ComparisonTableProps {
  banks: Bank[];
  criteria: Criterion[];
  data: ComparisonData;
}

// Mock data generator for demo
const generateMockData = (banks: Bank[], criteria: Criterion[]): ComparisonData => {
  const data: ComparisonData = {};
  
  banks.forEach((bank) => {
    data[bank.id] = {};
    criteria.forEach((criterion) => {
      // Sber has slightly better chances
      const chance = bank.id === "sber" ? 0.75 : 0.6;
      data[bank.id][criterion.id] = Math.random() > chance;
    });
  });
  
  return data;
};

export const ComparisonTable = ({ banks, criteria, data }: ComparisonTableProps) => {
  // Use provided data or generate mock data for demo
  const tableData = Object.keys(data).length > 0 ? data : generateMockData(banks, criteria);
  
  // Calculate best performer for each criterion
  const getBestForCriterion = (criterionId: string): string[] => {
    const bankIds = banks.map((b) => b.id);
    return bankIds.filter((bankId) => tableData[bankId]?.[criterionId]);
  };

  return (
    <Card className="overflow-hidden animate-fade-in">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="sticky left-0 z-20 bg-muted/50 min-w-[200px] font-semibold">
                Критерий
              </TableHead>
              {banks.map((bank) => (
                <TableHead
                  key={bank.id}
                  className={`text-center min-w-[120px] ${
                    bank.id === "sber" ? "bg-primary/10 font-semibold" : ""
                  }`}
                >
                  <div className="flex flex-col items-center gap-2 py-2">
                    <Building2 className={bank.id === "sber" ? "text-primary" : "text-muted-foreground"} />
                    <span className={bank.id === "sber" ? "text-primary" : ""}>{bank.name}</span>
                    {bank.id === "sber" && (
                      <Badge variant="secondary" className="text-xs bg-primary/20 text-primary">
                        Базовый
                      </Badge>
                    )}
                  </div>
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {criteria.map((criterion, index) => {
              const bestBanks = getBestForCriterion(criterion.id);
              
              return (
                <TableRow
                  key={criterion.id}
                  className={`transition-colors hover:bg-muted/30 ${
                    index % 2 === 0 ? "bg-background" : "bg-muted/10"
                  }`}
                >
                  <TableCell className="sticky left-0 z-10 bg-inherit font-medium">
                    {criterion.name}
                  </TableCell>
                  {banks.map((bank) => {
                    const hasFeature = tableData[bank.id]?.[criterion.id];
                    const isBest = bestBanks.length > 0 && hasFeature;
                    
                    return (
                      <TableCell
                        key={bank.id}
                        className={`text-center ${
                          isBest ? "bg-success/10" : ""
                        } ${bank.id === "sber" ? "bg-primary/5" : ""}`}
                      >
                        {hasFeature ? (
                          <div className="flex justify-center">
                            <Check className={`w-5 h-5 ${isBest ? "text-success animate-pulse-glow" : "text-primary"}`} />
                          </div>
                        ) : (
                          <div className="flex justify-center">
                            <X className="w-5 h-5 text-muted-foreground/40" />
                          </div>
                        )}
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
      
      {/* Data sources footer */}
      <div className="border-t border-border bg-muted/30 px-6 py-3 space-y-2">
        <p className="text-xs text-muted-foreground">
          <span className="font-medium">Источники данных:</span>
        </p>
        <div className="inline-flex gap-2 flex-wrap">
          <Badge variant="outline" className="text-xs">Banki.ru</Badge>
          <Badge variant="outline" className="text-xs">Sravni.ru</Badge>
          <Badge variant="outline" className="text-xs">Frankrg.com</Badge>
          <Badge variant="outline" className="text-xs">RBK.ru</Badge>
        </div>
        <p className="text-xs text-muted-foreground">Дата актуальности: {new Date().toLocaleDateString("ru-RU")}</p>
      </div>
    </Card>
  );
};
