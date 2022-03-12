### Tập dữ liệu văn bản OCR tiếng Anh
- Tập dữ liệu văn bản OCR tiếng Anh là một phần của bộ cơ sở dữ liệu văn bản OCR trong cuộc thi hậu xử lý văn bản OCR [1] của hội nghị quốc tế ICDAR 2017. Bộ cơ sở dữ liệu bao gồm các văn bản chuyên khảo và tạp chí định kỳ, trong đó một nửa là tiếng Anh và một nửa là tiếng Pháp.
- Mô hình được đánh giá trên tập văn bản chuyên khảo tiếng Anh, được chia thành 666 văn bản dùng để huấn luyện mô hình và 81 văn bản cho đánh giá mô hình. Các văn bản OCR và các văn bản gốc đúng Ground Truth (GT) đã được canh hàng ở mức ký tự và được cung cấp bởi ban tổ chức cuộc thi [[tải]](https://sites.google.com/view/icdar2017-postcorrectionocr/dataset?authuser=0).

### Tập dữ liệu văn bản OCR tiếng Việt
- Tập dữ liệu văn bản OCR tiếng Việt là kết quả đầu ra của mô hình mã hóa giải mã dựa trên cơ chế attention (gọi là mô hình AED) với bộ mã hóa sử dụng mạng DenseNet và bộ giải mã Long Short-Term Memory (LSTM) được đề xuất bởi nhóm tác giả Anh Duc Le et al. [2] (**Tác giả Anh Duc Le cũng là một thành viên của đề tài**).
- Đầu vào của mô hình AED là hình ảnh của các văn bản viết tay trực tuyến trong tập dữ liệu VNOnDB-Line của bộ cơ sở dữ liệu VNOnDB [[tải]](http://tc11.cvc.uab.es/datasets/HANDS-VNOnDB2018_1) [3], được sử dụng trong cuộc thi nhận dạng văn bản viết tay trực tuyến tiếng Việt [4]. Mô hình sử dụng bộ dữ liệu VNOnDB-Line với tập dữ liệu huấn luyện bao gồm 5662 dòng văn bản, trong khi tập dữ liệu đánh giá có 1634 dòng văn bản.
- Sau đó, chúng tôi tiếp tục thực hiện canh hàng bằng tay ở mức ký tự cho các văn bản OCR tiếng Việt và các văn bản gốc đúng GT tương ứng (tham khảo hình bên dưới). Tập dữ liệu văn bản OCR tiếng Việt đã được canh hàng có thể tải tại đây [[tập training]](https://drive.google.com/file/d/1RBg--_LDkEmM-5M2j81zgw5VQh8U5iKa/view?usp=sharing), [[tập validation]](https://drive.google.com/file/d/1l7JvSwaq0JhtODm8GYNTTT6prFUpjQ1_/view?usp=sharing), [[tập test]](https://drive.google.com/file/d/1Ui3Dk1blWOivkYJ7HkKOdV9H_NviBbF1/view?usp=sharing).

![alt text](https://github.com/ngu0029/post_ocr_models/blob/main/2.%20Datasets/char_alignment_vn.png)

### Tham khảo
[1] Chiron G, Doucet A, Coustaty M, Moreux J. 2017. ICDAR2017 Competition on Post-OCR Text Correction. 14th IAPR International Conference
on Document Analysis and Recognition (ICDAR) Kyoto, Japan 01:1423-1428, DOI 10.1109/ICDAR.2017.232

[2] **Le, A.D.**, Nguyen, H.T., Nakagawa, M. 2020. An End-to-End Recognition System for Unconstrained Vietnamese Handwriting. SN Computer Science 1(7). https://doi.org/10.1007/s42979-019-0001-4

[3] Nguyen, H.T., Nguyen, C.T., Pham, B.T., Nakagawa, M. 2018. A database of unconstrained Vietnamese online handwriting and recognition experiments by recurrent neural networks. Pattern Recognition 78, 291–306. https://doi.org/10.1016/j.patcog.2018.01.013

[4] Nguyen HT, Nguyen CT, Nakagawa M. 2018. ICFHR 2018 - Competition on Vietnamese Online Handwritten Text Recognition using HANDS-VNOnDB (VOHTR2018). 16th Int. Conf. on Frontiers in Handwriting Recognition (ICFHR), pp. 494–499.
