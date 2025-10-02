import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MetricChart = ({ data }) => {
  const MAX_ITEMS = 20;
  const fullLabels = Object.keys(data.result || {});
  const fullValues = Object.values(data.result || {});

  const values = fullValues.slice(0, MAX_ITEMS).map((v) => {
    if (typeof v === 'object' && v !== null) {
      const nums = Object.values(v).filter((val) => typeof val === 'number');
      return nums.length > 0 ? nums[0] : 0;
    }
    return typeof v === 'number' ? v : 0;
  });

  const labels = fullLabels.slice(0, MAX_ITEMS);

  const chartData = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: data.type_chart === 'line' ? 'rgba(92, 116, 240, 0.2)' : [
          '#8EC9DB',
          '#5C74F0',
          '#A3D5F7',
          '#7AA7F2',
          '#B3E0FF',
          '#4F6CE0',
        ],
        borderColor: data.type_chart === 'line' ? '#5C74F0' : '#fff',
        borderWidth: data.type_chart === 'line' ? 3 : 2,
        borderRadius: 8,
        hoverOffset: 8,
        tension: data.type_chart === 'line' ? 0.4 : 0,
        pointRadius: data.type_chart === 'line' ? 4 : 0,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(30, 58, 138, 0.9)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#3B82F6',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 10,
      },
    },
    scales: data.type_chart === 'pie' ? {} : {
      x: {
        grid: { display: false, drawBorder: false, drawTicks: false },
        ticks: {
          callback: (val, index) =>
            labels[index].length > 7
              ? labels[index].substr(0, 7) + '…'
              : labels[index],
        },
      },
      y: {
        grid: { display: false, drawBorder: false, drawTicks: false },
        beginAtZero: true,
      },
    },
  };

  if (data.type_chart === 'pie') {
    return <Pie data={chartData} options={options} />;
  } else if (data.type_chart === 'line') {
    return <Line data={chartData} options={options} />;
  } else {
    return <Bar data={chartData} options={options} />;
  }
};

export default MetricChart;
