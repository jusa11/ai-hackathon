

export const setMessage = async (
  systemPrompt,
  userPrompt = '',
  mode,
  service,
  context
) => {
  try {
    const response = await service.chat({
      messages: [
        {
          role: 'system',
          content: systemPrompt,
        },
        ...context,
        {
          role: 'user',
          content: userPrompt,
        },
      ],
    });

    return (
      response.choices?.[0]?.message?.content ||
      'Нет ответа от Джейсона Стэтхэма'
    );
  } catch (error) {
    console.error(`Ошибка при запросе к ${mode}:`, error);
    return `${mode} сейчас не может вам ответить. Пожалуйста, попробуйте позже.`;
  }
};
