#include<iostream>
#include <ctime>

using namespace std;

class Animal {
public:
    Animal(int h, int b, int t)
    {
        hunger = h;
        bored = b;
        tired = t;
    }
    void Eat(int=5);
    void Sleep(int=5);
    int Dead();
    int hunger, bored, tired;
    void passTime(int=1);
};

class Cat : public Animal{
public:
    Cat(int h=1, int b=1, int t=1): Animal(h, b, t)
    {srand(time(NULL));}
    void Play(int=3);
    void Trick();
    void Speak();
    void Hunt(int=3, int=4);
    void Dress();
    void MyMood();
private:
    static const int NTRICKS=3;
    static const string sTRICKS[NTRICKS];
    static const int NDRESS=2;
    static const string sDress[NDRESS];
    static const int NHUNT=3;
    static const string sHunting[NHUNT];
};

void help()
{
    cout << "0. Quit the game\n";
    cout << "1. Sleep\n";
    cout << "2. Play\n";
    cout << "3. Speak\n";
    cout << "4. Perform trick\n";
    cout << "5. Hunt\n";
    cout << "6. Eat\n";
    cout << "7. Dress\n";
    cout << "8. Help\n";
}

const string Cat::sTRICKS[NTRICKS] = {"jump", "juggle", "roll over"};
const string Cat::sHunting[NHUNT] = {"fly", "butterfly", "bird"};
const string Cat::sDress[NDRESS] = {"green t-shirt", "cool glasses"};

void Cat::MyMood()
{
    cout << "---------------------\n";
    cout << "Hunger: " << hunger << '\n';
    cout << "Boredom: " << bored << '\n';
    cout << "Tiredness: " << tired << '\n';
    cout << "---------------------\n";
}

int Animal::Dead()
{
    if ((hunger >= 10) & (bored >= 10) & (tired >= 10)) {cout << "Unfortunately, your cat is dead:(\n"; return 1;}
}

void Animal::passTime(int t)
{
    hunger += t;
    bored += t;
    tired += t;
}

void Animal::Sleep(int s)
{
    passTime();
    cout << "Zzzzz..\n";
    bored += s;
    tired -= s;
    if (bored>=10) bored=10;
    if (tired<0) tired=0;
}

void Animal::Eat(int food)
{
    hunger -= food;
    if (hunger<0) hunger=0;
    cout << "Yammmy\nThanks, now I'm not so hungry:P\n";
}

void Cat::Hunt(int food, int p)
{
    hunger += food;
    tired += p;
    if (hunger>=10) hunger=10;
    if (tired>=10) tired=10;
    string prey = sHunting[rand()%NHUNT];
    cout << "I have caught a huge " << prey << "! Did you see it? 0_0\n";
}

void Cat::Play(int p)
{
    passTime();
    cout << "This is fun:D Love sunbeams so much!\n";
    bored -= p;
    tired += p;
    if (tired>=10) tired=10;
    if (bored<0) bored=0;
}

void Cat::Speak()
{
    cout << "Meeeeoooow\n";
}

void Cat::Trick()
{
    if (tired<5) {
        string myTrick = sTRICKS[rand()%NTRICKS];
        cout << "Check this trick " << myTrick << "! I trained it for so long..\n";
        tired++;
        if (tired>=10) tired=10;
    }
    else {
        cout << "No trick for you >-<\n";
    }
}

void Cat::Dress()
{
    bored--;
    if (bored<0) bored=0;
    string dress = sDress[rand()%NDRESS];
    cout << "Woow! In this " << dress << " I look wonderful!\n";
}

int main()
{
    Cat *MyCat;
    MyCat = new Cat();
    char action;

    cout << "Welcome to the game!\n";
    cout << "Here you can take care of your cat. Watch your pet mood (hunger, boredom and tiredness) to keep it alive!\n\n";
    MyCat->MyMood();

    help();

    do {
        cout << "\n\nEnter number of action:\n";
        cin >> action;
        if      ((MyCat->Dead()) == 1) break;
        if      (action=='0') cout << "Goodbye!\nYour pet gonna die, if you exit the game:(\n";
        else if (action=='1') {MyCat->Sleep(); MyCat->MyMood();}
        else if (action=='2') {MyCat->Play(); MyCat->MyMood();}
        else if (action=='3') {MyCat->Speak(); MyCat->MyMood();}
        else if (action=='4') {MyCat->Trick(); MyCat->MyMood();}
        else if (action=='5') {MyCat->Hunt(); MyCat->MyMood();}
        else if (action=='6') {MyCat->Eat(); MyCat->MyMood();}
        else if (action=='7') {MyCat->Dress(); MyCat->MyMood();}
        else if (action=='8') help();
        else cout << "Wrong enter.. Try another number of action\n";
    } while (action != '0');

    delete MyCat;

    return 0;
}
