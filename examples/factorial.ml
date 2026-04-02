int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int num;
    int result;
    
    read(num);
    result = factorial(num);
    print(result);
    
    return 0;
}
