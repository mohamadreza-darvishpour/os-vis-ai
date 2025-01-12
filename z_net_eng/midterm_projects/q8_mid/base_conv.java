// کتابخانه ی اسکنر برای دریافت ورودی
import java.util.Scanner;

//کلاس اصلی همنام با فایل
public class base_conv{

//تابع اصلی با دسترسی پویا و خروجی نامعلوم
public static void main(String[] args){

// حلقه ی بی نهایت برای تست ورودی های مختلف
while(true){
//دستورات درون ترای انجام میشوند در صورت خطا دستورات درون اکسپشن
try{
// ساخت شی اسکنر با کانستراکتور سیستم این
Scanner scn  = new Scanner(System.in);
// نمایش پیغام مناسب
System.out.print("\nEnter integer number : ");
// ذخیره ی ورودی در متغیر
int num = scn.nextInt();
System.out.print("original:" + num + "<> base 2 :"+ret_str_num_base(num , 2) + " <> base 16 : " +ret_str_num_base(num , 16) );
// در صورت خطا دستورات این بخش انجام میشود
}catch(Exception e){
System.out.println("wrong inputted amount. try again.");
}
}
}






// یک تابع با دریافت دو آرگومان عدد مبنای 10 و بیس برای تغییر 
public static String ret_str_num_base(int number , int base){

// اگر 0 بود همان 0 را ارسال میکند.
if(number==0){
return "0";
}
// ذخیره ی عدد موقت برای تغییرات بعدی
int temp = number;
String result = "" ;
// مثبت کردن عدد موقت برای انجام تقسیم بر بیس 
if(number<0){
temp = -1 * temp;
}
// کاراکتر های ذخیره شده برای بیس تا شانزده
String[] digits = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"};


// انجام تقسیمات متوالی و محاسبه ی باقیمانده بر بیس جدید
while(temp > 0){
//ذخیره باقیمانده
int remain = temp % base ;
// اضافه کردن معادل کاراکتری باقیمانده به استرینگ 
result = result + (digits[remain]);
//تقسیم کردن برای محاسبه ی دوباره ی باقیمانده
temp /= base;
}

//اگر منفی بود یک کاراکتر منفی به انتها اضاف میکنیم.
if(number<0){
result = result + "-";
}

//با یک حلقه ی فور استرینگ را معکوس میکنیم تا عدد بدست بیاید
String rev_str = "";
for (int i = result.length()-1 ; i>=0 ; i--){
rev_str = rev_str + result.charAt(i);
}
//ارسال به خروجی
return rev_str;
}




}













