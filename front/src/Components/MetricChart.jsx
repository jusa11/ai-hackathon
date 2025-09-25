import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const MetricChart = ({ data, big }) => {
  const MAX_ITEMS = 20;
  const fullLabels = Object.keys(data.result || {});
  const fullValues = Object.values(data.result || {});

  // Нормализация значений — если вложенный объект, берём первое числовое значение
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
        backgroundColor: [
          '#8EC9DB',
          '#5C74F0',
          '#A3D5F7',
          '#7AA7F2',
          '#B3E0FF',
          '#4F6CE0',
        ],
        borderColor: '#1E3A8A',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { mode: 'index', intersect: false },
    },
    scales: {
      x: {
        ticks: {
          callback: (val, index) => {
            const label = labels[index];
            return label.length > 5 ? label.substr(0, 5) + '...' : label;
          },
        },
      },
      y: { beginAtZero: true },
    },
  };

  return data.type_chart === 'pie' ? (
    <Pie data={chartData} options={options} />
  ) : (
    <Bar data={chartData} options={options} />
  );
};

export default MetricChart;
