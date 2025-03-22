import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download } from 'lucide-react';
import styles from './FileView.module.css';
import { useFiles } from '../hooks/useFile';

const FileView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [file, setFile] = useState<{ url: string; type: string; name: string } | null>(null);
  const [textContent, setTextContent] = useState<string>('');

  const {files} = useFiles();

  useEffect(() => {
    const foundFile = files.find(file => file.id === id);
    if(foundFile) {
      setFile(foundFile);
      if (foundFile.type === 'text/plain' || foundFile.type === 'application/json') {
        fetch(foundFile.url)
          .then(response => response.text())
          .then(content => {
            if (foundFile.type === 'application/json') {
              try {
                const formatted = JSON.stringify(JSON.parse(content), null, 2);
                setTextContent(formatted);
              } catch (e) {
                setTextContent(content);
              }
            } else {
              setTextContent(content);
            }
          })
          .catch(error => {
            console.error('Error loading file content:', error);
            setTextContent('Error loading file content');
          });
      }
    }else{
      navigate('/');
    }
  }, [id, files]);

  if (!file) {
    return null;
  }

  const handleDownload = () => {
    // Create a temporary anchor element
    const downloadLink = document.createElement('a');
    downloadLink.href = file.url;
    downloadLink.download = file.name;
    
    // Append to the document, click it, and then remove it
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  };

  const renderContent = () => {
    if (file.type.startsWith('image/')) {
      return (
        <div className={styles.imageContainer}>
          <img src={file.url} alt={file.name} className={styles.image} />
        </div>
      );
    }

    if (file.type === 'text/plain' || file.type === 'application/json') {
      return (
        <pre className={styles.textContent}>
          {textContent}
        </pre>
      );
    }

    return <p>Unsupported file type</p>;
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Link to="/" className={styles.backButton}>
          <ArrowLeft />
          <span>Back to Files</span>
        </Link>
        <button onClick={handleDownload} className={styles.downloadButton}>
          <Download />
          <span>Download</span>
        </button>
      </div>
      <div className={styles.content}>
        <h2 className={styles.title}>{file.name}</h2>
        {renderContent()}
      </div>
    </div>
  );
};

export default FileView;