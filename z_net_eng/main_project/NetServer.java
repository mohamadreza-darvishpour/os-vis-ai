import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class NetServer {
    private static final String CONFIG_FILE = "server_config.txt";
    private static final String FILES_FOLDER = "files_to_answer";

    private static int synRequestLimit;
    private static int portToRun;
    private static Set<String> blockedIPs;
    private static Set<String> restrictedIPs;

    private static ThreadPoolExecutor threadPool;

    public static void main(String[] args) throws IOException {
        loadConfig();
        threadPool = (ThreadPoolExecutor) Executors.newFixedThreadPool(synRequestLimit);

        // Monitor config file for changes
        new Thread(NetServer::monitorConfigFile).start();

        try (ServerSocket serverSocket = new ServerSocket(portToRun)) {
            System.out.println("Server is running on port " + portToRun + "...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                threadPool.execute(() -> handleClient(clientSocket));
            }
        } catch (IOException e) {
            System.err.println("Server error: " + e.getMessage());
        }
    }

    private static void loadConfig() throws IOException {
        Properties config = new Properties();
        try (BufferedReader reader = new BufferedReader(new FileReader(CONFIG_FILE))) {
            config.load(reader);

            synRequestLimit = Integer.parseInt(config.getProperty("syn_request_limit", "3"));
            portToRun = Integer.parseInt(config.getProperty("port_to_run_answer", "2030"));

            blockedIPs = parseList(config.getProperty("blocked_ip", "[]"));
            restrictedIPs = parseList(config.getProperty("restricted_ip", "[]"));

            System.out.println("Config loaded: syn_request_limit=" + synRequestLimit + ", port_to_run_answer=" + portToRun);
        } catch (Exception e) {
            throw new IOException("Error loading configuration: " + e.getMessage());
        }
    }

    private static void monitorConfigFile() {
        File configFile = new File(CONFIG_FILE);
        long lastModified = configFile.lastModified();

        while (true) {
            try {
                Thread.sleep(2000);
                if (configFile.lastModified() != lastModified) {
                    lastModified = configFile.lastModified();
                    System.out.println("Config file changed, reloading...");
                    loadConfig();
                }
            } catch (Exception e) {
                System.err.println("Error monitoring config file: " + e.getMessage());
            }
        }
    }

    private static Set<String> parseList(String list) {
        list = list.replaceAll("[\\[\\]\\s]", "");
        if (list.isEmpty()) {
            return new HashSet<>();
        }
        return new HashSet<>(Arrays.asList(list.split(",")));
    }

    private static void handleClient(Socket clientSocket) {
        String clientIP = clientSocket.getInetAddress().getHostAddress();
        if (blockedIPs.contains(clientIP)) {
            closeSocket(clientSocket);
            return;
        }

        try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()))) {

            String requestLine = in.readLine();
            if (requestLine == null || requestLine.trim().isEmpty()) {
                sendErrorResponse(out, "400.html");
                return;
            }

            String[] requestParts = requestLine.split(" ");
            if (requestParts.length < 2) {
                sendErrorResponse(out, "400.html");
                return;
            }

            String method = requestParts[0];
            String fileName = requestParts[1].substring(1); // Remove leading '/'

            if (restrictedIPs.contains(clientIP)) {
                sendErrorResponse(out, "403.html");
                return;
            }

            File requestedFile = new File(FILES_FOLDER, fileName);
            if (!requestedFile.exists() || !requestedFile.isFile()) {
                sendErrorResponse(out, "404.html");
                return;
            }

            sendFileResponse(out, requestedFile);

        } catch (Exception e) {
            System.err.println("Error handling client: " + e.getMessage());
        } finally {
            closeSocket(clientSocket);
        }
    }

    private static void sendErrorResponse(BufferedWriter out, String errorFile) throws IOException {
        File errorPage = new File(FILES_FOLDER, errorFile);
        if (errorPage.exists() && errorPage.isFile()) {
            sendFileResponse(out, errorPage);
        } else {
            out.write("HTTP/1.1 500 Internal Server Error\r\n\r\n");
            out.write("<h1>500 Internal Server Error</h1>");
            out.flush();
        }
    }

    private static void sendFileResponse(BufferedWriter out, File file) throws IOException {
        out.write("HTTP/1.1 200 OK\r\n\r\n");
        try (BufferedReader fileReader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = fileReader.readLine()) != null) {
                out.write(line);
                out.newLine();
            }
        }
        out.flush();
    }

    private static void closeSocket(Socket socket) {
        try {
            socket.close();
        } catch (IOException e) {
            System.err.println("Error closing socket: " + e.getMessage());
        }
    }

    // Testing with curl:
    // 1. Start the server.
    // 2. Open a terminal and type: curl http://localhost:2030/index_page.html
    // 3. Observe the response or error message based on the request and IP.
}
