import java.io.*;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletResponse;

public class ServletInitializer extends HttpServlet
{
	
    /**
	 * 
	 */
	private static final long serialVersionUID = 4919834643536923947L;
    //mySys.writeLog("log");

    public void init() throws ServletException
    {    	
    	System.out.println("Servlet Initialized successfully");
    }

    public void service(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException
    {
    	System.out.println("Servlet service successfully");
    }
}