import MetricChart from './MetricChart';

const MetricCard = ({ metric, big }) => {
  return (
    <div className="bg-white p-4 shadow-md rounded-3xl border border-gray-300">
      {metric?.data && (
        <>
          <div className="metric-title">{metric.data.title}</div>
          <div className="metric-chart max-h-52">
            <MetricChart data={metric.data} big={big} />
          </div>
        </>
      )}
    </div>
  );
};

export default MetricCard;
