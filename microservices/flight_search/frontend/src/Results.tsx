import { Card, CardContent, CardDescription, CardHeader, CardFooter, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";

function toTime12h(datetime: string) {
  const date = new Date(datetime.replace(" ", "T"))
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  }).format(date)
}

function durationToHoursMinutes(duration: number) {
  return `${Math.floor(duration / 60)}h ${duration % 60}m`;
}

const Flight = ({ flightInfo }: any) => {
  return (
    <div>
      <div>
        <p className="text-xs gray">Flight No. {flightInfo.flight_number}</p>
      </div>
      <div className="flex justify-between items-center">
        <div className="flex flex-col">
          <span>{flightInfo.departure_airport.id}</span>
          <span>{toTime12h(flightInfo.departure_airport.time)}</span>
        </div>

        <div className="flex flex-col items-center">
          <Separator className="w-24" />
          <span className="text-xs">{durationToHoursMinutes(flightInfo.duration)}</span>
          <Separator className="w-24" />
        </div>

        <div className="flex flex-col">
          <span>{flightInfo.arrival_airport.id}</span>
          <span>{toTime12h(flightInfo.arrival_airport.time)}</span>
        </div>
      </div>
    </div>
  );
};

const Layover = ({ layoverInfo }: any) => {
  return (
    <div className="flex justify-center py-2">
      <Badge>{durationToHoursMinutes(layoverInfo.duration)} Layover — {layoverInfo.name} ({layoverInfo.id})</Badge>
    </div>
  );
};

function FlightResult({ flightInfo }: any) {
  const informationOrder = [];
  const numFlights = flightInfo.flights.length;
  if (flightInfo.hasOwnProperty("layovers")) {
    const numLayovers = flightInfo.layovers.length;
    let i = 0;
    let j = 0;
    while (i < numFlights) {
      informationOrder.push({
        type: "flight",
        info: flightInfo.flights[i],
      });
      if (j < numLayovers
        && flightInfo.layovers[j].id == flightInfo.flights[i].arrival_airport.id) {
        informationOrder.push({
          type: "layover",
          info: flightInfo.layovers[j]
        });
        j++;
      }
      i++;
    }
  } else {
    for (let i = 0; i < numFlights; ++i) {
      informationOrder.push({
        type: "flight",
        info: flightInfo.flights[i],
      });
    }
  }
  console.log(informationOrder);
  return (
    // <Card className="min-w-[30vw]">
    <Card className="">
      <CardHeader>
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <img src={flightInfo.airline_logo} />
          </div>
          <p>Price — ${flightInfo.price}</p>
        </div>
      </CardHeader>
      <CardContent>
        {informationOrder.map((item: any) => {
          if (item.type == "flight") {
            return <Flight flightInfo={item.info} />
          }
          if (item.type == "layover") {
            return (
              <>
                <Layover layoverInfo={item.info} />
                <Separator />
              </>
            );
          }
        })}
      </CardContent>
    </Card>
  );
}

export function Results({ results }: any) {
  const resultsError = results && (results.hasOwnProperty("error") || results.hasOwnProperty("errors"));
  const resultsErrorMessage = resultsError
    ? (results.error == "Google Flights hasn't returned any results for this query."
      ? "No results returned for this query."
      : results.error)
    : "";

  return (
    <div className="w-full flex justify-center items-center gap-4">
      {resultsError && <p>{resultsErrorMessage}</p>}
      {!resultsError && results &&
        <div className="w-full flex flex-col justify-center gap-4">
          <h2 className="text-xl font-semibold tracking-tight text-center">Best departing flights</h2>
          <div className="
            w-[80%]
            mx-auto
            grid
            grid-cols-2
            sm:grid-cols-1 
            lg:grid-cols-2 
            xl:grid-cols-2 
            gap-4
          ">
            {results.best_flights && results.best_flights.map((flight: any) => {
              return <FlightResult flightInfo={flight} />;
            })}
          </div>
          <Separator />
          <h2 className="text-xl font-semibold tracking-tight text-center">Other departing flights</h2>
          <div className="
            w-[80%]
            mx-auto
            grid
            grid-cols-2
            sm:grid-cols-1 
            lg:grid-cols-2 
            xl:grid-cols-2 gap-4">
            {results.best_flights && results.other_flights.map((flight: any) => {
              return <FlightResult flightInfo={flight} />;
            })}
          </div>
        </div>
      }
    </div>
  )
}