export const download = (fileName: string, href: string) => {
  const link = document.createElement("a");
  link.href = href;

  link.setAttribute("download", fileName);
  document.body.appendChild(link);
  link.click();
  link.parentNode?.removeChild(link);
  window.URL.revokeObjectURL(href);
};
