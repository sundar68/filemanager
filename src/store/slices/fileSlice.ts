import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { filesApi } from '../../services/api';
import { FileState, FileUploadBody } from '../../types/fileType';

const initialState: FileState = {
    loading: false,
    files: [],
    error: null,
    isUploading: false,
};

export const fetchFiles = createAsyncThunk(
    'files/fetchFiles',
    async (_, { rejectWithValue }) => {
        try {
            const response = await filesApi.getFiles();
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.message || 'Failed to fetch files.');
        }
    }
);

export const uploadFile = createAsyncThunk(
    'files/uploadFile',
    async (body : FileUploadBody, { rejectWithValue }) => {
        try {
            const response = await filesApi.uploadFile(body);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.message || 'Failed to upload file.');
        }
    }
);

const fileSlice = createSlice({
    name: 'files',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
      builder
        .addCase(fetchFiles.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(fetchFiles.fulfilled, (state, action) => {
          state.loading = false;
          state.files = action.payload.files;
        })
        .addCase(fetchFiles.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload as string;
        })
        .addCase(uploadFile.pending, (state) => {
          state.isUploading = true;
          state.error = null;
        })
        .addCase(uploadFile.fulfilled, (state, action) => {
          state.isUploading = false;
          state.files.push(action.payload);
        })
        .addCase(uploadFile.rejected, (state, action) => {
          state.isUploading = false;
          state.error = action.payload as string;
        })
        ;
    },
  });


export default fileSlice.reducer;