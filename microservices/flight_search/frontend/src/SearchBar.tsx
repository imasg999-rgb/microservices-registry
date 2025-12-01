"use client"
import { useState } from "react";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover"
import { ChevronDownIcon } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Calendar } from "@/components/ui/calendar";

// https://medium.com/@naveenalla3000/how-to-install-all-components-of-shadcn-ui-in-one-command-bun-setup-9f2fe1e959bc

const formSchema = z.object({
  origin_code: z.string().length(3),
  destination_code: z.string().length(3),
  departure_date: z
    .string()
    .regex(/\d{4}\-\d{2}-\d{2}/, "Use format YYYY-MM-DD")
    .refine((val) => {
      const [y, m, d] = val.split("-").map(Number);
      if (!y || !m || !d) return false;
      const date = new Date(y, m-1, d);
      return (
        date.getFullYear() == y
        && date.getMonth() + 1 == m
        && date.getDate() == d
      );
    }),
  return_date: z
    .string()
    .regex(/\d{4}\-\d{2}-\d{2}/, "Use format YYYY-MM-DD")
    .refine((val) => {
      const [y, m, d] = val.split("-").map(Number);
      if (!y || !m || !d) return false;
      const date = new Date(y, m-1, d);
      return (
        date.getFullYear() == y
        && date.getMonth() + 1 == m
        && date.getDate() == d
      );
    }),
});

type SearchBarProps = {
  onSearch: (values: {
    origin_code: string
    destination_code: string
    departure_date: string
    return_date: string
  }) => void
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      origin_code: "YYZ",
      destination_code: "AUS",
      departure_date: "",
      return_date: "",
    },
  });
  const [date1Open, setDate1Open] = useState(false);
  const [date2Open, setDate2Open] = useState(false);

  function onSubmit(values: z.infer<typeof formSchema>) {
    onSearch(values);
  }

  return (
    <div className="w-full flex justify-center border-b bg-background p-4">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 flex items-center gap-4">
          {/* Origin Airport code */}
          <FormField
            control={form.control}
            name="origin_code"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Origin Airport</FormLabel>
                <FormControl>
                  <Input placeholder="shadcn" {...field} />
                </FormControl>
                <FormDescription>
                  IATA Airport code
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* Destination airport code */}
          <FormField
            control={form.control}
            name="destination_code"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Destination Airport</FormLabel>
                <FormControl>
                  <Input placeholder="shadcn" {...field} />
                </FormControl>
                <FormDescription>
                  IATA Airport code
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* Origin date */}
          <FormField
            control={form.control}
            name="departure_date"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Departure Date</FormLabel>
                <FormControl>
                  {/* <Calendar
                    mode="single"
                    selected={field.value ? new Date(field.value) : undefined}
                    onSelect={(date) => {
                      if (date) field.onChange(date.toISOString().slice(0, 10))
                    }}
                  /> */}
                  <Popover open={date1Open} onOpenChange={setDate1Open}>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        id="date"
                        className="w-48 justify-between font-normal"
                      >
                        {field.value ?? "Select date"}
                        <ChevronDownIcon />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto overflow-hidden p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={
                          field.value
                            ? new Date(
                              Number(field.value.split("-")[0]),
                              Number(field.value.split("-")[1]) - 1,
                              Number(field.value.split("-")[2])
                            )
                            : undefined}
                        captionLayout="dropdown"
                        onSelect={(date) => {
                          if (!date) return
                          const year = date.getFullYear()
                          const month = String(date.getMonth() + 1).padStart(2, "0")
                          const day = String(date.getDate()).padStart(2, "0")
                          field.onChange(`${year}-${month}-${day}`)

                          setDate1Open(false)
                        }}
                      />
                    </PopoverContent>
                  </Popover>
                </FormControl>
                <FormDescription>
                  The date of departure from the origin airport.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* Return date */}
          <FormField
            control={form.control}
            name="return_date"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Return Date</FormLabel>
                <FormControl>
                  <Popover open={date2Open} onOpenChange={setDate2Open}>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        id="date"
                        className="w-48 justify-between font-normal"
                      >
                        {field.value ?? "Select date"}
                        <ChevronDownIcon />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto overflow-hidden p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={
                          field.value
                            ? new Date(
                              Number(field.value.split("-")[0]),
                              Number(field.value.split("-")[1]) - 1,
                              Number(field.value.split("-")[2])
                            )
                            : undefined}
                        captionLayout="dropdown"
                        onSelect={(date) => {
                          if (!date) return
                          const year = date.getFullYear()
                          const month = String(date.getMonth() + 1).padStart(2, "0")
                          const day = String(date.getDate()).padStart(2, "0")
                          field.onChange(`${year}-${month}-${day}`)
                          setDate2Open(false)
                        }}
                      />
                    </PopoverContent>
                  </Popover>
                </FormControl>
                <FormDescription>
                  The date of departure from the origin airport.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit">Submit</Button>
        </form>
      </Form>
    </div>
  );
}

export default SearchBar;
