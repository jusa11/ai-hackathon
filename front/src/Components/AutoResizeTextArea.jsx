import { useRef, useEffect } from 'react';

const AutoResizeTextarea = ({
  value,
  onChange,
  maxHeight = 200,
  handleSubmit,
  setQuery,
}) => {
  const textareaRef = useRef(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
    }
  }, [value, maxHeight]);

  return (
    <textarea
      ref={textareaRef}
      value={value}
      onChange={onChange}
      onKeyDown={(e) => {
        // Отправка по Enter, перенос строки по Shift+Enter
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault(); // отменяем перенос строки
          handleSubmit(e);
        }
      }}
      placeholder="Введите ваш вопрос"
      className="border rounded-3xl w-full p-3 pr-16 resize-none 
                 focus:outline-none focus:ring-0 overflow-hidden"
      style={{ maxHeight: `${maxHeight}px` }}
      rows={1}
    />
  );
};

export default AutoResizeTextarea;
