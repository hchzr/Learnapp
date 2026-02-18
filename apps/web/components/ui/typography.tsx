import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const typographyVariants = cva("text-slate-950 dark:text-slate-50", {
  variants: {
    variant: {
      h1: "text-3xl font-bold tracking-tight",
      h2: "text-2xl font-semibold tracking-tight",
      lead: "text-base text-slate-700 dark:text-slate-300",
      body: "text-sm text-slate-600 dark:text-slate-300"
    }
  },
  defaultVariants: {
    variant: "body"
  }
});

export interface TypographyProps extends React.HTMLAttributes<HTMLParagraphElement>, VariantProps<typeof typographyVariants> {
  as?: "h1" | "h2" | "p";
}

export function Typography({ as = "p", variant, className, ...props }: TypographyProps) {
  const Comp = as;

  return <Comp className={cn(typographyVariants({ variant }), className)} {...props} />;
}
