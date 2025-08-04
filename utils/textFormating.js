export default function textFormating(text) {
  if (!text) return '';

  return text.replace(/([_*\[\]()~`>#+\-=|{}.!\\])/g, '\\$1');
}
