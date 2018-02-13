# cvcutter

### Usage

Command line tool:
`python cvcutter.py [folder-with-images-to-cut]`

Also jupyter notebook for cool graphics and debug

### Dependencies

* `numpy`
* `cv2`

For .ipynb also `matplotlib`

### Example (from ipyNB)
![1](https://user-images.githubusercontent.com/5108025/36148601-be3b0ffc-10cd-11e8-9b7e-923983b290e5.png)

`src\2016-03-09 15.14.29.jpg : (1520L, 2688L, 3L) => [10.752  6.08 ]`

	Trying to fix zeros on 775 :
		[-0.0125      0.          0.00657895]  -> 
		[-1.25000000e-02 -8.22368421e-05  6.57894737e-03]
	
`borders:  6 [0, 526, 775, 844, 1128, 2058]`

![2](https://user-images.githubusercontent.com/5108025/36148602-be5be542-10cd-11e8-9ad9-43c4350da9b4.png)

`borders:  2 [195, 888]`

![3](https://user-images.githubusercontent.com/5108025/36148603-be836c20-10cd-11e8-9311-e45cdbaa3df4.png)
![4](https://user-images.githubusercontent.com/5108025/36148605-be9e7a74-10cd-11e8-83a4-2b14b8e03e98.png)
![5](https://user-images.githubusercontent.com/5108025/36148606-bebf9cfe-10cd-11e8-8467-28d9a82b3551.png)

