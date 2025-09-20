import { useRef, useState } from 'react';

const AutoResizeTextarea = ({ maxHeight = 200 }) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);

  const handleChange = (e) => {
    const textarea = textareaRef.current;
    setValue(e.target.value);
		console.log(textareaRef);

    if (textarea) {
      textarea.style.height = 'auto'; // сброс
      textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
    }
  };

  return (
    <textarea
      ref={textareaRef}
      value={value}
      onChange={handleChange}
      placeholder="Введите ваш вопрос"
      className="border rounded-3xl w-full p-3 pr-16 resize-none 
                 focus:outline-none focus:ring-0 overflow-hidden"
      style={{ maxHeight: `${maxHeight}px` }}
      rows={1}
    />
  );
};

export default AutoResizeTextarea;
