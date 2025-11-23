import { 
  CreditCard, 
  PiggyBank, 
  FileText, 
  Wallet,
  TrendingUp,
  Building 
} from "lucide-react";
import { Card } from "@/components/ui/card";

export interface Product {
  id: string;
  name: string;
  icon: typeof CreditCard;
}

export const PRODUCTS: Product[] = [
  { id: "deposits", name: "Вклады", icon: PiggyBank },
  { id: "credits", name: "Кредиты", icon: Wallet },
  { id: "cards", name: "Карты", icon: CreditCard },
  { id: "tariffs", name: "Тарифы", icon: FileText },
  { id: "mortgage", name: "Ипотека", icon: Building },
  { id: "investments", name: "Инвестиции", icon: TrendingUp },
];

interface ProductSelectorProps {
  selectedProduct: string | null;
  onChange: (productId: string) => void;
}

export const ProductSelector = ({ selectedProduct, onChange }: ProductSelectorProps) => {
  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-foreground">
        Продукт для анализа
      </label>
      
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {PRODUCTS.map((product) => {
          const Icon = product.icon;
          const isSelected = selectedProduct === product.id;
          
          return (
            <Card
              key={product.id}
              className={`
                p-4 cursor-pointer transition-all duration-200
                hover:shadow-md hover:scale-[1.02]
                ${
                  isSelected
                    ? "bg-primary text-primary-foreground border-primary shadow-md scale-[1.02]"
                    : "bg-card hover:bg-muted/50 border-border"
                }
              `}
              onClick={() => onChange(product.id)}
            >
              <div className="flex flex-col items-center gap-2 text-center">
                <Icon className={`w-6 h-6 ${isSelected ? "text-primary-foreground" : "text-primary"}`} />
                <span className="text-sm font-medium">{product.name}</span>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
