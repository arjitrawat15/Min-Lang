int main() {
    int n;
    int a;
    int b;
    int temp;
    int i;
    
    a = 0;
    b = 1;
    
    read(n);
    
    for (i = 0; i < n; i = i + 1) {
        print(a);
        temp = a + b;
        a = b;
        b = temp;
    }
    
    return 0;
}
