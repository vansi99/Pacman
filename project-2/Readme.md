# Project2

## Câu 1

Hàm evaluation em tính dựa trên khoảng cách nhỏ nhất giữa food và pacman với khoảng cách nhỏ nhất của con ma gần nhất với pacman nhất và điểm của state đó.

## Câu 2

a. Đầu tiên là khởi tạo tất cả các action pacman có thể đi tìm maximize value của các action dựa vào hàm minimax và trả lại action đó.

b. Thuật toán minimax, áp dụng đệ quy với điều kiện dừng khi game lose, win hay độ sâu đã tới mức yêu cầu thì trả lại điểm tại vị trí đó qua các agent và sử dụng các hàm min_val để tính giá trị min action của các đối thủ xung quanh khi mà cây hiện tại đã quét đủ agent xung quanh mà độ sâu chưa đạt thì mình lại sử dụng max_val để tạo độ sâu mới với những action tiếp theo của pacman 

## Câu 3

Tương tự câu 2 nhưng mình sẽ khởi tạo thêm 2 biến alpha và beta.
Tại mỗi hàm max_val nếu điểm tính được của mỗi state lớn hơn beta thì chấm dứt và trả lại giá trị đó luôn nếu không cập nhật alpha nếu giá trị đó lơn hơn alpha hiện tại. 
Tương tự với min_val thì nếu giá trị nhỏ hơn alpha thì trả lại giá trị đó nếu không cập nhật beta nếu giá trị đó nhỏ hơn beta 

## Câu 4

Tương tự câu 2 nhưng thuật toán expectimax thì ta sẽ trả về trung bình điểm số của các state xung quanh đối thủ 

## Câu 5

Hàm betterevaluation của em tính dựa trên hàm tuyến tính 

Điểm state mang lại + khoảng cách food gần nhất * hệ số food + khoảng cách ma * hệ số ma + khoảng cách điểm mà ăn vào ma sẽ bị vô hiệu * hệ số 