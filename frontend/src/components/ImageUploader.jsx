import React, { useRef, useState } from "react";

const ACCEPTED_TYPES = ["image/jpeg", "image/jpg", "image/png"];

export default function ImageUploader({ imagePreview, onFileSelect, onClear }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFiles = (fileList) => {
    const file = fileList && fileList[0];
    if (file && ACCEPTED_TYPES.includes(file.type)) {
      onFileSelect(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleClick = () => {
    inputRef.current?.click();
  };

  if (imagePreview) {
    return (
      <div className="upload-zone" style={{ flexDirection: "column", gap: "0.6rem" }}>
        <img
          src={imagePreview}
          alt="Selected leaf preview"
          style={{
            maxHeight: "160px",
            width: "auto",
            borderRadius: "10px",
            objectFit: "contain"
          }}
        />
        <div className="upload-zone-text">Image selected</div>
        <button
          type="button"
          className="nutri-button"
          style={{ width: "auto", padding: "0.3rem 0.9rem" }}
          onClick={(e) => {
            e.stopPropagation();
            onClear();
            if (inputRef.current) inputRef.current.value = "";
          }}
        >
          Remove image
        </button>
      </div>
    );
  }

  return (
    <div
      className={`upload-zone ${isDragging ? "dragging" : ""}`}
      onClick={handleClick}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      role="button"
      tabIndex={0}
    >
      <span className="upload-zone-text">
        Drop leaf image here — JPG, JPEG or PNG
      </span>
      <input
        ref={inputRef}
        type="file"
        accept=".jpg,.jpeg,.png"
        style={{ display: "none" }}
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  );
}
