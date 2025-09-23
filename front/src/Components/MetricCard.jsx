import MetricChart from './MetricChart';

const MetricCard = ({ metric, big, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-gray-200 p-4 shadow-md rounded-3xl border border-gray-300 animate-pulse">
        <div className="h-52 animate-pulse"></div>
      </div>
    );
  }

  if (metric?.data) {
    return (
      <div className="bg-white p-4 shadow-md rounded-3xl border border-gray-300 ">
        <div>{metric.data.title}</div>
        <div className="metric-chart max-h-52">
          <MetricChart data={metric.data} big={big} />
        </div>
      </div>
    );
  }

  return null;
};

export default MetricCard;
