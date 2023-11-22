#include <iostream>
#include <vector>

class TernaryHeap {
private:
    std::vector<int> heap;

    // Helper function to get parent index
    static int parent(int i) {
        return (i - 1) / 3;
    }

    // Helper function to get children indices
    std::vector<int> children(int i) {
        std::vector<int> childrenIndices;
        for (int j = 1; j <= 3; ++j) {
            int childIndex = 3 * i + j;
            if (childIndex < heap.size()) {
                childrenIndices.push_back(childIndex);
            }
        }
        return childrenIndices;
    }

    // Helper function to maintain heap property upward
    void heapifyUp(int i) {
        while (i > 0 && heap[i] < heap[parent(i)]) {
            std::swap(heap[i], heap[parent(i)]);
            i = parent(i);
        }
    }

    // Helper function to maintain heap property downward
    void heapifyDown(int i) {
        int smallest = i;
        std::vector<int> childIndices = children(i);

        for (int childIndex : childIndices) {
            if (childIndex < heap.size() && heap[childIndex] < heap[smallest]) {
                smallest = childIndex;
            }
        }

        if (i != smallest) {
            std::swap(heap[i], heap[smallest]);
            heapifyDown(smallest);
        }
    }

public:
    // Insert an element into the heap
    void insert(int value) {
        heap.push_back(value);
        heapifyUp(heap.size() - 1);
    }

    // Get the minimum element in the heap
    int getMin() {
        if (heap.empty()) {
            std::cerr << "Heap is empty\n";
            return -1; // Or throw an exception
        }
        return heap[0];
    }

    // Heapify the heap starting from index i
    void heapify(int i) {
        if (i >= 0 && i < heap.size()) {
            heapifyDown(i);
        } else {
            std::cerr << "Index out of bounds\n";
        }
    }

    // Delete the minimum element from the heap
    void deleteMin() {
        if (heap.empty()) {
            std::cerr << "Heap is empty\n";
            return; // Or throw an exception
        }

        heap[0] = heap.back();
        heap.pop_back();
        heapifyDown(0);
    }

    // Build a heap from an array
    void buildHeap(const std::vector<int>& array) {
        heap = array;
        for (int i = (heap.size() - 1) / 3; i >= 0; --i) {
            heapifyDown(i);
        }
    }
};

int main() {
    TernaryHeap heap;

    // Example usage
    heap.insert(4);
    heap.insert(8);
    heap.insert(2);
    heap.insert(6);
    heap.insert(10);

    std::cout << "Min element: " << heap.getMin() << std::endl;

    heap.deleteMin();

    std::cout << "Min element after deletion: " << heap.getMin() << std::endl;

    std::vector<int> arrayToBuildHeap = {3, 7, 1, 9, 5};
    heap.buildHeap(arrayToBuildHeap);

    std::cout << "Min element after building heap: " << heap.getMin() << std::endl;

    return 0;
}
