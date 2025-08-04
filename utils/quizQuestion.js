const quizQuestion = [
  {
    question: 'Что такое HTTP?',
    options: [
      { text: 'Протокол передачи гипертекста', correct: true },
      { text: 'Язык программирования', correct: false },
      { text: 'База данных', correct: false },
      { text: 'Операционная система', correct: false },
    ],
    correctAnswer: 0,
  },
  {
    question: 'Принципом ООП НЕ является:',
    options: [
      { text: 'Полиморфизм', correct: false },
      { text: 'Наследование', correct: false },
      { text: 'Делегирование', correct: true },
      { text: 'Инкапсуляция', correct: false },
    ],
    correctAnswer: 2,
  },
  {
    question: 'Свойство функции обрабатывать данные разных типов называется:',
    options: [
      { text: 'Инкапсуляция', correct: false },
      { text: 'Полиморфизм', correct: true },
      { text: 'Наследование', correct: false },
      { text: 'Абстракция', correct: false },
    ],
    correctAnswer: 1,
  },
  {
    question:
      'Какой из перечисленных алгоритмов имеет временную сложность O(log n)?',
    options: [
      { text: 'Линейный поиск', correct: false },
      { text: 'Двоичный поиск', correct: true },
      { text: 'Сортировка пузырьком', correct: false },
      { text: 'Сортировка вставками', correct: false },
    ],
    correctAnswer: 1,
  },
  {
    question: 'В IP-заголовок записывается:',
    options: [
      { text: 'IP-адрес отправителя и получателя', correct: true },
      { text: 'Информация о формате передаваемого файла', correct: false },
      { text: 'MAC-адрес устройства', correct: true },
      { text: 'URL адрес запрашиваемого ресурса', correct: false },
    ],
    correctAnswer: 0,
  },
  {
    question: 'Какое двоичное представление числа 143?',
    options: [
      { text: '10101111', correct: false },
      { text: '10001111', correct: true },
      { text: '11110001', correct: false },
      { text: '11011111', correct: false },
    ],
    correctAnswer: 1,
  },
  {
    question: 'ALU — это:',
    options: [
      { text: 'Арифметико-логическое устройство', correct: true },
      { text: 'Адресное пространство памяти', correct: false },
      { text: 'Язык программирования', correct: false },
      { text: 'Тип процессора', correct: false },
    ],
    correctAnswer: 0,
  },
];

export default quizQuestion;
