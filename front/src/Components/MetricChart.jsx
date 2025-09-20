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

// Регистрируем компоненты Chart.js
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
  const labels = Object.keys(data.result || {});
  const values = Object.values(data.result || {});

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
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        ticks: {
          callback: function (value) {
            const label = this.getLabelForValue(value);
            return label.length > 5 ? label.substr(0, 5) + '...' : label;
          },
        },
      },
    },
  };

  // Для больших графиков можно добавить padding или изменить размеры шрифта
  if (big) {
    options.plugins.tooltip.titleFont = { size: 16 };
    options.plugins.tooltip.bodyFont = { size: 14 };
  }

  return data.type_chart === 'pie' ? (
    <Pie data={chartData} options={options} />
  ) : (
    <Bar data={chartData} options={options} />
  );
};

export default MetricChart;
