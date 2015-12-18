#if __cplusplus < 201103L
    #error "should use C++11 implementation"
#endif

#include <iostream>
#include <climits>
#include <cstdio>

using namespace std;

int main()
{
    long long ll_min = LLONG_MIN;
    long long ll_max = LLONG_MAX;
    unsigned long long ull_max = ULLONG_MAX;
    cout<<ll_min<<endl;
    cout<<ll_max<<endl;
    cout<<ull_max<<endl;
    return 0;
}
