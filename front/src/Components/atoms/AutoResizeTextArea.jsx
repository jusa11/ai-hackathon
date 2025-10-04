import { useRef, useEffect, useState } from 'react';

const AutoResizeTextarea = ({
  value,
  onChange,
  maxHeight = 200,
  handleSubmit,
}) => {
  const textareaRef = useRef(null);
  const [isOverflow, setIsOverflow] = useState(false);
  const randomPlaceHolder = [
    'Спросите что-нибудь, например: "Cредний стаж работы сотрудников в компании"',
    'Спросите о том, что хотите узнать. Например: "Средний возраст сотрудников"',
    'Спросите, что нибудь, например: "Количество сотрудников по регионам"',
    'Спросите о том, что хотите узнать. Например: "Средний срок работы до увольнения"',
    'Могу узнать для вас средний опыт сотрудников в департаменте...',
    'Спросите что-нибудь, например: "Количество сотрудников по форме работы офис/удаленка"',
    'Могу узнать для вас, например текучесть кадров за определенный месяц',
  ];

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      const newHeight = textarea.scrollHeight;
      textarea.style.height = `${Math.min(newHeight, maxHeight)}px`;
      setIsOverflow(newHeight > maxHeight);
    }
  }, [value, maxHeight]);

  const randomPlaceHolderForForm = () => {
    const randomIndex = Math.floor(Math.random() * randomPlaceHolder.length);
    return randomPlaceHolder[randomIndex];
  };

  return (
    <textarea
      ref={textareaRef}
      value={value}
      onChange={onChange}
      onKeyDown={(e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSubmit(e);
        }
      }}
      placeholder={randomPlaceHolderForForm()}
      className={`border rounded-3xl w-full p-3 pr-16 resize-none 
                  focus:outline-none focus:ring-0 min-h-12 ${
                    isOverflow ? 'overflow-y-auto' : 'overflow-hidden'
                  }`}
      style={{ maxHeight: `${maxHeight}px` }}
      rows={1}
    />
  );
};

export default AutoResizeTextarea;
