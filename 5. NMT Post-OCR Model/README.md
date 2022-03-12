###	Mô hình dịch máy sử dụng mạng nơron học sâu
Mô hình NMT đề xuất bao gồm hai mạng sử dụng bộ nhớ dài-ngắn hạn hai chiều (Bidirectional long short-term memory), một cho bộ mã hóa và một cho bộ giải mã. Bộ mã hóa đọc văn bản OCR dưới dạng chuỗi các từ đầu vào và xuất ra một vectơ ngữ cảnh duy nhất. Bộ giải mã đọc vectơ ngữ cảnh để tạo ra văn bản đầu ra đã được sửa lỗi. Cơ chế chú ý cho phép bộ giải mã tập trung vào một phần khác nhau của đầu ra của bộ mã hóa cho mỗi bước của chuỗi các từ đầu ra của bộ giải mã. Các giai đoạn xử lý của mô hình NMT bao gồm:
- Tiền xử lý (canh hàng và tách từ - alignment and tokenization)
- Phát hiện lỗi (error detection)
- Sửa lỗi (error correction)
