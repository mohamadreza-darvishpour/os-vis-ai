//فراخوانی لیست و اری لیست برای ذخیره ی مقادیر
import java.util.List;
import java.util.ArrayList;
//فراخوانی کالکشن برای ذخیره ی مقادیر متفاوت در یک دستور
import java.util.Collections;


// ساخت کلاس اصلی همنام با فایل
public class concat_list{

//ساخت تابع اصلی کلاس اصلی برای اجرا 
public static void main(String[] args){
// ساخت یک لیست چند متغیره از اشیا که مقادیر به صورت اشیا در آن ذخیره میشوند.
List<Object> temp_list = new ArrayList<>();
// ذخیره ی مقادیر متفاوت به صورت شی در لیست
Collections.addAll(temp_list , 1,2,"first",8.9,-2,"second" ,true);
// خروجی گرفتن از تابعی که لیست اشیا را به عنوان ورودی گرفته و خروجی یک استرینگ است.
String con_str = ret_str_of_list(temp_list);
// نمایش با پیغام مناسب
System.out.println( "Sample list : " + temp_list + "\nResult : \"" + con_str + "\"");
}

// تابع پویا برای دسترسی در کلاس بدون ساخت شی  ورودی یک لیست ابجکت و خروجی استرینگ
public static String ret_str_of_list(List<Object> test_list){
//ساخت استرینگ خالی اولیه برای ذخیره ی مقدار
String concatenated = "" ;
//ایتریت کردن در بین ایتم های لیست
for(Object item : test_list){
// با استفاده از جمع با استرینگ شی ذخیره شده به صورت استرینگ برگردانده میشود
concatenated = concatenated + item ;
}
//ارسال استرینگ به خروجی
return concatenated;
}


}


