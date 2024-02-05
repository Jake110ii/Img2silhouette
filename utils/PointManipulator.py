import numpy as np

class PointManipulator:
    def __init__(self, existing_x, existing_y):
        self.existing_x = existing_x
        self.existing_y = existing_y

    def calculate_distance(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def find_best_insertion_point(self, new_x, new_y):
        min_distance_sum = float('inf')
        best_index = 0

        for i in range(len(self.existing_x) + 1):
            temp_x = self.existing_x[:i] + [new_x] + self.existing_x[i:]
            temp_y = self.existing_y[:i] + [new_y] + self.existing_y[i:]
            distance_sum = sum(self.calculate_distance(temp_x[j], temp_y[j], temp_x[j+1], temp_y[j+1]) for j in range(len(temp_x)-1))

            if distance_sum < min_distance_sum:
                min_distance_sum = distance_sum
                best_index = i

        return best_index

    def insert_new_point(self, new_x, new_y):
        best_index = self.find_best_insertion_point(new_x, new_y)
        new_x_list = self.existing_x[:best_index] + [new_x] + self.existing_x[best_index:]
        new_y_list = self.existing_y[:best_index] + [new_y] + self.existing_y[best_index:]
        return new_x_list, new_y_list


def main():
    # 例として、既存の点と新しい点を設定
    existing_x = [1, 2, 4, 7, 9, 12, 15, 17, 20, 22]
    existing_y = [3, 6, 8, 11, 13, 16, 18, 21, 23, 26]
    new_x = 10
    new_y = 10

    # PointManipulator クラスのインスタンスを作成
    point_manipulator = PointManipulator(existing_x, existing_y)

    # 新しい点を挿入した後の座標リストを取得
    new_x_list, new_y_list = point_manipulator.insert_new_point(new_x, new_y)

    # 結果の表示
    print("Existing X:", existing_x)
    print("Existing Y:", existing_y)
    print("New X List:", new_x_list)
    print("New Y List:", new_y_list)


def sort_shortest_distance(existing_x, existing_y, new_x, new_y):
    point_manipulator = PointManipulator(existing_x, existing_y)
    new_x_list, new_y_list = point_manipulator.insert_new_point(new_x, new_y)
    
#    new_x_list = np.array(new_x_list)
#    new_y_list = np.array(new_y_list)
    return new_x_list, new_y_list


if __name__ == "__main__":
    main()


