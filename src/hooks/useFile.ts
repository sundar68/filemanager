import { useSelector, useDispatch } from 'react-redux';
import type { AppDispatch, RootState } from '../store/store';
import { fetchFiles, uploadFile } from '../store/slices/fileSlice';
import { FileUploadBody } from '../types/fileType';

export function useFiles() {
    const dispatch: AppDispatch = useDispatch();
    const files = useSelector((state: RootState) => state.files);
  
    const getFiles = async () => {
      try {
        await dispatch(fetchFiles()).unwrap();
      } catch (error) {
        throw error;
      }
    };

    const uploadFileAction = async (body: FileUploadBody) => {
        try {
          await dispatch(uploadFile(body)).unwrap();
        } catch (error) {
          throw error;
        }
      }
  
    return {
      files : files.files,
      fileLoading: files.loading,
      fileError: files.error,
      isUploading: files.isUploading,
      getFiles,
      uploadFileAction,
    };
  }