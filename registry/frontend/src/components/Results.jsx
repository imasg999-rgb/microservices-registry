import "./Results";

const ServiceEntry = () => {
  return <div>Pretend service</div>;
};

export function Results({ services }) {
  return (
    <div className="results">
      <ul>
        {services && services.map(service => <ServiceEntry service={service} />)}
      </ul>
    </div>
  );
}