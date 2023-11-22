#include<iostream>

#include<list>

#include<algorithm>

#include<climits>

using namespace std;

struct Node

{

    int data, degree;

    Node *child, *sibling, *parent;

};

class BHeap

{

    list<Node*> heap;

public:

    Node *newNode(int key)

    {

        Node *temp = new Node;

        temp->data = key;

        temp->degree = 0;

        temp->child = temp->parent = temp->sibling = NULL;

        return temp;

    }

    Node *mergeBTrees(Node *b1, Node *b2)

    {

        if (b1->data > b2->data)

            swap(b1, b2);

        b2->parent = b1;

        b2->sibling = b1->child;

        b1->child = b2;

        b1->degree++;

        return b1;

    }

    list<Node *> Union(list<Node *> &h1,

                       list<Node *> &h2)

    {

        list<Node *> _new;

        list<Node *>::iterator it = h1.begin();

        list<Node *>::iterator ot = h2.begin();

        while (it != h1.end() && ot != h2.end())

        {

            if ((*it)->degree <= (*ot)->degree)

            {

                _new.push_back(*it);

                it++;

            }

            else

            {

                _new.push_back(*ot);

                ot++;

            }

        }

        while (it != h1.end())

        {

            _new.push_back(*it);

            it++;

        }

        while (ot != h2.end())

        {

            _new.push_back(*ot);

            ot++;

        }

        return _new;

    }

    void adjust()

    {

        if (heap.size() <= 1)

            return ;

        list<Node *> newheap;

        list<Node *>::iterator it1, it2, it3;

        it1 = it2 = it3 = heap.begin();

        if (heap.size() == 2)

        {

            it2 = it1;

            it2++;

            it3 = heap.end();

        }

        else

        {

            it2++;

            it3 = it2;

            it3++;

        }

        while (it1 != heap.end())

        {

            if (it2 == heap.end())

                it1++;

            else if ((*it1)->degree < (*it2)->degree)

            {

                it1++;

                it2++;

                if (it3 != heap.end())

                    it3++;

            }

            else if (it3 != heap.end() &&

                     (*it1)->degree == (*it2)->degree &&

                     (*it1)->degree == (*it3)->degree)

            {

                it1++;

                it2++;

                it3++;

            }

            else if ((*it1)->degree == (*it2)->degree)

            {

                Node *temp;

                *it1 = mergeBTrees(*it1, *it2);

                it2 = heap.erase(it2);

                if (it3 != heap.end())

                    it3++;

            }

        }

    }

    void insertTree(Node *tree)

    {

        list<Node *> temp;

        temp.push_back(tree);

        heap = Union(heap, temp);

        adjust();

    }

    void insert(int key)

    {

        Node *temp = newNode(key);

        insertTree(temp);

    }

    list<Node *> removeMinTree(Node *tree)

    {

        list<Node *> _heap;

        Node *temp = tree->child;

        Node *lo;

        while (temp)

        {

            lo = temp;

            temp = temp->sibling;

            lo->sibling = NULL;

            _heap.push_front(lo);

        }

        return _heap;

    }

    Node *getMin()

    {

        list<Node *>::iterator it = heap.begin();

        Node *temp = *it;

        while (it != heap.end())

        {

            if ((*it)->data < temp->data)

                temp = *it;

            it++;

        }

        return temp;

    }

    void extractMin()

    {

        list<Node *> newheap, lo;

        Node *temp;

        temp = getMin();

        list<Node *>::iterator it;

        it = heap.begin();

        while (it != heap.end())

        {

            if (*it != temp)

            {

                newheap.push_back(*it);

            }

            it++;

        }

        lo = removeMinTree(temp);

        heap = Union(newheap, lo);

        adjust();

    }

    Node * findNode(Node * it, int val)

    {

        if (it == NULL)

            return NULL;

        if (it->data == val)

            return it;

        if(it->data > val)

            return NULL;

        Node *res = findNode(it->child, val);

        if (res != NULL)

            return res;

        return findNode(it->sibling, val);

    }

    void decreaseKey( int old_val,

                      int new_val)

    {

        list<Node *>::iterator it=heap.begin();

        Node *node = NULL;

        while (it != heap.end() && node == NULL)

        {

            node = findNode(*it, old_val);

            it++;

        }

        if (node == NULL)

            return;

        node->data = new_val;

        Node *parent = node->parent;

        while (parent != NULL && node->data < parent->data)

        {

            swap(node->data, parent->data);

            node = parent;

            parent = parent->parent;

        }

    }

    void Delete(int val)

    {

        decreaseKey(val, INT_MIN);

        extractMin();

    }

    void printTree(Node *h)

    {

        while (h)

        {

            cout << h->data << " ";

            printTree(h->child);

            h = h->sibling;

        }

    }

    void printHeap()

    {

        list<Node *>::iterator it;

        it = heap.begin();

        while (it != heap.end())

        {

            printTree(*it);

            it++;

        }

        cout<<"\n";

    }

};

int main()

{

    int ch,key;

    BHeap H;

    H.insert(9);

    H.insert(4);

    H.insert(17);

    H.insert(10);

    H.insert(8);

    cout<< "Heap elements after insertion:\n";

    H.printHeap();

    Node *temp = H.getMin();

    cout << "Minimum element "

         << temp->data << "\n";

    H.decreaseKey(17,5);

    temp = H.getMin();

    cout << "Now Minimum element of heap "<< temp->data << "\n";

    H.extractMin();

    cout << "Heap after deletion of minimum element\n";

    H.printHeap();

    H.Delete(4);

    cout << "Heap after deletion \n";

    H.printHeap();

    return 0;

}