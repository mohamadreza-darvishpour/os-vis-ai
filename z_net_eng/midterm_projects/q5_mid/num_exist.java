// استفاده از اسکنر برای دریافت ورودی 
import java.util.Scanner;
// فراخوانی تابع لیست و آرایه برای ثبت اعداد
import java.util.List;
import java.util.ArrayList;

// ساخت کلاس اصلی با نام برابر با فایل
public class num_exist{

// ساخت تابعد اصلی کلاس اصلی به صورت پویا و خروجی نامعین
public static void main(String[] args){
// حلقه ی وایل بی نهایت برای امتحان ورودی های مختلف
while(true){
// استفاده از ترای برای جلوگیری از خارج شدن از برنامه به دلیل ورودی های نامناسب
try{
// ساخت یک لیست از اینتجر برای ذخیره ی اعداد
// اعداد توسط فانکشن پایین دریافت شده و لیست آنها برگردانده میشود
List<Integer> int_list = ret_list_till_negative() ;
// نمایش پیغام برای عدد سرچ دریافتی
System.out.print("Enter a number for search: ");
// ساخت یک شی اسکنر برای دریافت عدد ورودی با کانستراکتور سیستم این
Scanner scan_obj = new Scanner(System.in);
// فراخوانی اینپوت برای دریافت اینتجر
int search_num = scan_obj.nextInt();
// پیام بودن یا نبودن در لیست.
String has_message = " has not ";
// حلقه ی فور برای مقایسه ی تک تک اعضای لیست با ورودی برای سرچ
for (int item : int_list){
// اگر برابر پیدا شد پیام تغییر کند.
if(item == search_num){
has_message = " has ";
// با بریک از لوپ خارج شود اگر برابر پیدا شد
break;
}
}
// نمایش نتیجه ی نهایی
System.out.print("Result:  " + int_list + has_message + search_num + " .\n\n");

//در صورت بروز خطا در ترای دستورات این بخش که شامل نمایش پیغام مناسب است چاپ میشود
}catch(Exception e ){
System.out.println("wrong entered amount. try again.\n");
}
}

}



// فانکشن استاتیک برای دسترسی در کلاس حاضر بدون ساخت شی و ارسال یک لیست از اینتجر به خروجی
public static List<Integer> ret_list_till_negative(){
// ساخت لیست برای ذخیره ی اعداد دریافتی
List<Integer> temp_list = new ArrayList<>() ;
// ساخت متغیر ها برای شماره ی عدد ورودی و ذخیره ی آن
int temp_num ,counter=0 ;
// استفاده از دو.وایل برای حد اقل یک اجرا پس از آن بررسی شرط
do{
// اضافه کردن یکی به شمارنده هر بار
counter = counter +1 ;
// دریافت عدد مورد نظر اینت به وسیله ی تابع نوشته شده ی پایین با یک ورودی که شماره ی عدد است.
temp_num = ret_nth_num(counter);
// ذخیره شدن فقط در صورتی که منفی نباشد. 
if(temp_num > -1){
// ذخیره ی عدد ورودی
temp_list.add(temp_num);
}
// دستورات بالا حداقل یک بار اجرا شده سپس شرط بررسی میشودد که نباید عدد منفی باشد.
}while(temp_num > -1);

//ارسال لیست ساخته شده به خروجی 
return temp_list;
}


// یک تابع برای دریافت راحت تر ورودی ان ام با یک پیام مناسب
public static int ret_nth_num(int n ){
//ساخت شی اسکنر که در بالا یک بار توضیح داده شد.
Scanner my_scanner = new Scanner(System.in) ;
System.out.print("Enter number #" + n + ": ");
int num = my_scanner.nextInt();
return num;
}


}






