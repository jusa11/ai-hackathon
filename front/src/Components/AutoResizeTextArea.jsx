import { useRef, useEffect, useState } from 'react';

const AutoResizeTextarea = ({
  value,
  onChange,
  maxHeight = 200,
  handleSubmit,
}) => {
  const textareaRef = useRef(null);
  const [isOverflow, setIsOverflow] = useState(false);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      const newHeight = textarea.scrollHeight;
      textarea.style.height = `${Math.min(newHeight, maxHeight)}px`;
      setIsOverflow(newHeight > maxHeight);
    }
  }, [value, maxHeight]);

  return (
    <textarea
      ref={textareaRef}
      value={value}
      onChange={onChange}
      onKeyDown={(e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          handleSubmit(e);
        }
      }}
      placeholder="Введите ваш вопрос"
      className={`border rounded-3xl w-full p-3 pr-16 resize-none 
                  focus:outline-none focus:ring-0 min-h-12 ${
                    isOverflow ? "overflow-y-auto" : "overflow-hidden"
                  }`}
      style={{ maxHeight: `${maxHeight}px` }}
      rows={1}
    />
  );
};

export default AutoResizeTextarea;
