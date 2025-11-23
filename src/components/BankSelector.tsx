import { useState } from "react";
import { Building2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export interface Bank {
  id: string;
  name: string;
  logo?: string;
}

const AVAILABLE_BANKS: Bank[] = [
  { id: "sber", name: "Сбербанк" },
  { id: "vtb", name: "ВТБ" },
  { id: "alpha", name: "Альфа-Банк" },
  { id: "tinkoff", name: "Тинькофф" },
  { id: "gazprom", name: "Газпромбанк" },
  { id: "raiffeisen", name: "Райффайзенбанк" },
  { id: "rosbank", name: "Росбанк" },
  { id: "mts", name: "МТС Банк" },
  { id: "otkritie", name: "Банк Открытие" },
  { id: "psb", name: "ПСБ" },
];

interface BankSelectorProps {
  selectedBanks: Bank[];
  onChange: (banks: Bank[]) => void;
}

export const BankSelector = ({ selectedBanks, onChange }: BankSelectorProps) => {
  const [open, setOpen] = useState(false);

  const toggleBank = (bank: Bank) => {
    const isSelected = selectedBanks.some((b) => b.id === bank.id);
    if (isSelected) {
      onChange(selectedBanks.filter((b) => b.id !== bank.id));
    } else {
      onChange([...selectedBanks, bank]);
    }
  };

  const removeBank = (bankId: string) => {
    onChange(selectedBanks.filter((b) => b.id !== bankId));
  };

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-foreground">
        Банки для сравнения
      </label>
      
      <div className="flex flex-wrap gap-2 min-h-[2.5rem]">
        {selectedBanks.map((bank) => (
          <Badge
            key={bank.id}
            variant="secondary"
            className="pl-3 pr-1 py-1.5 text-sm bg-primary/10 text-primary border-primary/20 hover:bg-primary/20 transition-colors"
          >
            <Building2 className="w-3 h-3 mr-1.5" />
            {bank.name}
            <Button
              variant="ghost"
              size="sm"
              className="h-auto p-1 ml-1 hover:bg-primary/30"
              onClick={() => removeBank(bank.id)}
            >
              <X className="w-3 h-3" />
            </Button>
          </Badge>
        ))}
        
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              size="sm"
              className="border-dashed border-primary/30 text-primary hover:bg-primary/10 hover:text-primary transition-colors"
            >
              + Добавить банк
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-[300px] p-0" align="start">
            <Command>
              <CommandInput placeholder="Поиск банка..." />
              <CommandList>
                <CommandEmpty>Банк не найден</CommandEmpty>
                <CommandGroup>
                  {AVAILABLE_BANKS.map((bank) => {
                    const isSelected = selectedBanks.some((b) => b.id === bank.id);
                    return (
                      <CommandItem
                        key={bank.id}
                        onSelect={() => {
                          toggleBank(bank);
                          setOpen(false);
                        }}
                        className={isSelected ? "opacity-50" : ""}
                      >
                        <Building2 className="w-4 h-4 mr-2 text-primary" />
                        {bank.name}
                        {isSelected && (
                          <span className="ml-auto text-xs text-muted-foreground">
                            ✓
                          </span>
                        )}
                      </CommandItem>
                    );
                  })}
                </CommandGroup>
              </CommandList>
            </Command>
          </PopoverContent>
        </Popover>
      </div>
      
      <p className="text-xs text-muted-foreground">
        Выбрано: {selectedBanks.length} {selectedBanks.length === 0 ? "банков" : selectedBanks.length === 1 ? "банк" : "банка"}
      </p>
    </div>
  );
};
