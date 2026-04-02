int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main() {
    int x;
    int y;
    int sum;
    int product;
    
    read(x);
    read(y);
    
    sum = add(x, y);
    product = multiply(x, y);
    
    print(sum);
    print(product);
    
    return 0;
}
