import "./Results.css";

const ServiceEntry = ({ service }) => {
  return (
    <div className="service-result flex flex-row">
      <div className="service-details">
        <p className="service-name">{service.name}</p>
        <p className="service-description">{service.description}</p>
      </div>
      <a className="service-link" href={service.url}>Open</a>
    </div>
  );
};

export function Results({ services }) {
  return (
    <div className="results">
      {services && services.map(service => <ServiceEntry service={service} key={service.id}/>)}
    </div>
  );
}