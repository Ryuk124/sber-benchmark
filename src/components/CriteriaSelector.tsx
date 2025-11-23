import { useState } from "react";
import { Plus, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";

export interface Criterion {
  id: string;
  name: string;
  custom?: boolean;
}

const DEFAULT_CRITERIA: Criterion[] = [
  { id: "cost", name: "Стоимость обслуживания" },
  { id: "sms", name: "СМС-уведомления" },
  { id: "withdrawal", name: "Снятие наличных в других банках" },
  { id: "transfers", name: "Переводы по реквизитам в другие банки" },
  { id: "interest", name: "Процент на остаток" },
  { id: "limit", name: "Кредитный лимит" },
  { id: "rate", name: "Процентные ставки" },
  { id: "payment", name: "Первоначальный взнос" },
  { id: "loyalty", name: "Программа лояльности" },
  { id: "cashback", name: "Кэшбэк" },
  { id: "grace", name: "Льготный период" },
];

interface CriteriaSelectorProps {
  selectedCriteria: Criterion[];
  onChange: (criteria: Criterion[]) => void;
}

export const CriteriaSelector = ({ selectedCriteria, onChange }: CriteriaSelectorProps) => {
  const [customCriterion, setCustomCriterion] = useState("");
  const [showInput, setShowInput] = useState(false);

  const toggleCriterion = (criterion: Criterion) => {
    const isSelected = selectedCriteria.some((c) => c.id === criterion.id);
    if (isSelected) {
      onChange(selectedCriteria.filter((c) => c.id !== criterion.id));
    } else {
      onChange([...selectedCriteria, criterion]);
    }
  };

  const addCustomCriterion = () => {
    if (customCriterion.trim()) {
      const newCriterion: Criterion = {
        id: `custom-${Date.now()}`,
        name: customCriterion.trim(),
        custom: true,
      };
      onChange([...selectedCriteria, newCriterion]);
      setCustomCriterion("");
      setShowInput(false);
    }
  };

  const removeCustomCriterion = (id: string) => {
    onChange(selectedCriteria.filter((c) => c.id !== id));
  };

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-foreground">
        Критерии сравнения
      </label>

      {/* Selected Custom Criteria */}
      {selectedCriteria.some((c) => c.custom) && (
        <div className="flex flex-wrap gap-2">
          {selectedCriteria
            .filter((c) => c.custom)
            .map((criterion) => (
              <Badge
                key={criterion.id}
                variant="secondary"
                className="pl-3 pr-1 py-1.5 text-sm bg-secondary/20 text-secondary border-secondary/30"
              >
                {criterion.name}
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-auto p-1 ml-1 hover:bg-secondary/30"
                  onClick={() => removeCustomCriterion(criterion.id)}
                >
                  <X className="w-3 h-3" />
                </Button>
              </Badge>
            ))}
        </div>
      )}

      {/* Default Criteria */}
      <ScrollArea className="h-[240px] rounded-md border border-border bg-card p-4">
        <div className="space-y-3">
          {DEFAULT_CRITERIA.map((criterion) => {
            const isSelected = selectedCriteria.some((c) => c.id === criterion.id);
            return (
              <div key={criterion.id} className="flex items-center space-x-3">
                <Checkbox
                  id={criterion.id}
                  checked={isSelected}
                  onCheckedChange={() => toggleCriterion(criterion)}
                  className="data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                />
                <label
                  htmlFor={criterion.id}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                >
                  {criterion.name}
                </label>
              </div>
            );
          })}
        </div>
      </ScrollArea>

      {/* Add Custom Criterion */}
      {showInput ? (
        <div className="flex gap-2">
          <Input
            placeholder="Введите свой критерий..."
            value={customCriterion}
            onChange={(e) => setCustomCriterion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                addCustomCriterion();
              }
            }}
            className="flex-1"
          />
          <Button
            onClick={addCustomCriterion}
            size="sm"
            className="bg-secondary hover:bg-secondary-hover text-secondary-foreground"
          >
            Добавить
          </Button>
          <Button
            onClick={() => {
              setShowInput(false);
              setCustomCriterion("");
            }}
            size="sm"
            variant="outline"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      ) : (
        <Button
          onClick={() => setShowInput(true)}
          variant="outline"
          size="sm"
          className="border-dashed border-secondary/30 text-secondary hover:bg-secondary/10"
        >
          <Plus className="w-4 h-4 mr-2" />
          Добавить свой критерий
        </Button>
      )}

      <p className="text-xs text-muted-foreground">
        Выбрано: {selectedCriteria.length} критери{selectedCriteria.length === 1 ? "й" : "ев"}
      </p>
    </div>
  );
};
