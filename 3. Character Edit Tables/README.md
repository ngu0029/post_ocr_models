### Bảng chỉnh sửa ký tự 
- Các văn bản trong tập dữ liệu huấn luyện bao gồm các đoạn văn bản OCR và đoạn văn bản GT tương ứng đã được canh hàng ở mức ký tự. Các văn bản này được quét để tìm ra các cặp mẫu ký tự không giống nhau có chiều dài một hoặc hai ký tự giữa văn bản OCR và văn bản GT (các thống kê lỗi OCR chỉ ra rằng các lỗi OCR chủ yếu chứa các phép chỉnh sửa mẫu ký tự ngắn [1, 2]).
- Trong bảng chỉnh sửa ký tự, mỗi mẫu ký tự lỗi trong văn bản OCR tương ứng với một hoặc nhiều mẫu ký tự sửa lỗi tìm thấy trong văn bản GT, cùng với tần suất xuất hiện của chúng trong tập dữ liệu huấn luyện. Cụ thể trong quá trình sửa lỗi, mỗi từ lỗi OCR được kiểm tra để thay thế các mẫu ký tự lỗi trong từ lỗi bằng các mẫu ký tự sửa lỗi để tạo ra các từ sửa lỗi.
- Các phép chỉnh sửa mẫu ký tự bao gồm xóa, chèn và thay thế. Ví dụ: từ sửa lỗi “remembered” cho từ lỗi “reinemb.ered” chứa hai phép chỉnh sửa, phép xóa dấu chấm “.” và phép thay thế “in” → “m”.

### Tham khảo
[1] Nguyen DQ, Le AD, Phan MN, Zelinka I. 2020. An In-depth Analysis of OCR Errors for Unconstrained Vietnamese Handwriting. The 7th International Conference on Future Data and Security Engineering (FDSE 2020). Lecture Notes in Computer Science series 12466, pp. 448–461. (**Cùng nhóm tác giả đề tài**)

[2] Nguyen HTT, Jatowt A, Coustaty M, Nguyen VN, Doucet A. 2019. Deep Statistical Analysis of OCR Errors for Effective Post-OCR Processing. In: 2019 ACM/IEEE Joint Conf. on Digital Libraries (Champaign, IL, USA), pp. 29-38.
