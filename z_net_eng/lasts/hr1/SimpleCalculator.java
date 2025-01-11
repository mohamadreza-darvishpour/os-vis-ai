import java.util.Scanner;

public class SimpleCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String continueProgram = "y";

        while (continueProgram.equalsIgnoreCase("y")) {
            try {
                // first dig
                System.out.print("write first operand: ");
                double operand1 = Double.parseDouble(scanner.nextLine());

                //sec dig
                System.out.print("write second operand: ");
                double operand2 = Double.parseDouble(scanner.nextLine());

                //operand 
                System.out.print("write operator (+, -, *, /): ");
                String operator = scanner.nextLine();
                double result;

                // operands with switch  
                switch (operator) {
                    case "+":
                        result = operand1 + operand2;
                        System.out.println("Result => " + operand1 + " + " + operand2 + " = " + result);
                        break;
                    case "-":
                        result = operand1 - operand2;
                        System.out.println("Result => " + operand1 + " - " + operand2 + " = " + result);
                        break;
                    case "*":
                        result = operand1 * operand2;
                        System.out.println("Result => " + operand1 + " * " + operand2 + " = " + result);
                        break;
                    case "/":
                        if (operand2 == 0) {
                            System.out.println("Result => divide by zero");
                        } else {
                            result = operand1 / operand2;
                            System.out.println("Result => " + operand1 + " / " + operand2 + " = " + result);
                        }
                        break;
                    default:
                        System.out.println("Invalid operator! Please use +, -, *, or /.");
                }

            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid number.");
            }

            // continue 
            System.out.print("Continue (y/n)? ");
            continueProgram = scanner.nextLine();
        }

        System.out.println("Bye...");
        scanner.close();
    }
}
