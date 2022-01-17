export const saveLocalToken = (token) => localStorage.setItem("token", token);
export const getLocalToken = () => localStorage.getItem("token");
export const removeLocalToken = () => localStorage.removeItem("token");
export const autoDownloadFile = (response) => {
  const blob = new Blob([response.data], { type: "application/zip" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "data";
  link.click();
  URL.revokeObjectURL(link.href);
};
export const getErrorMessage = (error, fieldData) => {
  if (error.length) {
    switch (error[0].$validator) {
      case "required":
        return `${fieldData.name} is required.`;
      case "email":
        return "Not a valid email address.";
      case "minLength":
        return `${fieldData.name} must be at least ${fieldData.length} characters long.`;
      default:
        return error[0].$message;
    }
  }
  return "Placeholder"; // for visible/invisible
};
