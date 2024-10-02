Here's a C program that creates a remote access terminal with a graphical user interface (GUI) using the GTK+ library:
```c
#include <gtk/gtk.h>
#include <libssh/libssh.h>

// SSH session variables
ssh_session session;
ssh_channel channel;
int auth_list;
int port = 22;
char *user = "username";
char *password = "password";
char *host = "target_host";

// GUI variables
GtkWidget *window;
GtkWidget *text_view;
GtkWidget *text_buffer;
GtkTextIter start, end;

// Function to execute commands on the remote machine
void execute_command(char *command) {
    int rc;
    char buffer[256];
    int nbytes;

    rc = ssh_channel_request_exec(channel, command);
    if (rc != SSH_OK) {
        g_error("Error executing command: %s\n", ssh_get_error(session));
        return;
    }

    nbytes = ssh_channel_read(channel, buffer, sizeof(buffer), 0);
    if (nbytes < 0) {
        g_error("Error reading command output: %s\n", ssh_get_error(session));
        return;
    }

    gtk_text_buffer_get_start_iter(GTK_TEXT_BUFFER(text_buffer), &start);
    gtk_text_buffer_insert(GTK_TEXT_BUFFER(text_buffer), &start, buffer, nbytes);
}

// Function to initialize SSH session
void init_ssh() {
    int rc;

    session = ssh_new();
    if (session == NULL) {
        g_error("Error creating SSH session\n");
        return;
    }

    ssh_options_set(session, SSH_OPTIONS_HOST, host);
    ssh_options_set(session, SSH_OPTIONS_PORT, &port);
    ssh_options_set(session, SSH_OPTIONS_USER, user);

    rc = ssh_connect(session);
    if (rc != SSH_OK) {
        g_error("Error connecting to SSH server: %s\n", ssh_get_error(session));
        ssh_free(session);
        return;
    }

    rc = ssh_userauth_password(session, NULL, password);
    if (rc != SSH_AUTH_SUCCESS) {
        g_error("Error authenticating with password: %s\n", ssh_get_error(session));
        ssh_disconnect(session);
        ssh_free(session);
        return;
    }

    channel = ssh_channel_new(session);
    if (channel == NULL) {
        g_error("Error creating SSH channel\n");
        ssh_disconnect(session);
        ssh_free(session);
        return;
    }

    rc = ssh_channel_open_session(channel);
    if (rc != SSH_OK) {
        g_error("Error opening SSH channel: %s\n", ssh_get_error(session));
        ssh_channel_free(channel);
        ssh_disconnect(session);
        ssh_free(session);
        return;
    }
}

// Function to close SSH session
void close_ssh() {
    ssh_channel_close(channel);
    ssh_channel_free(channel);
    ssh_disconnect(session);
    ssh_free(session);
}

// Function to handle GUI events
void on_button_clicked(GtkWidget *widget, gpointer data) {
    char *command = (char *)data;
    execute_command(command);
}

// Function to create the GUI
void create_gui() {
    GtkWidget *vbox;
    GtkWidget *hbox;
    GtkWidget *button;

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Remote Access Terminal");
    gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);
    gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_container_add(GTK_CONTAINER(window), vbox);

    text_view = gtk_text_view_new();
    text_buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
    gtk_box_pack_start(GTK_BOX(vbox), text_view, TRUE, TRUE, 0);

    hbox = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 5);
    gtk_box_pack_start(GTK_BOX(vbox), hbox, FALSE, FALSE, 0);

    button = gtk_button_new_with_label("Run Command");
    g_signal_connect(button, "clicked", G_CALLBACK(on_button_clicked), "ls");
    gtk_box_pack_start(GTK_BOX(hbox), button, FALSE, FALSE, 0);

    button = gtk_button_new_with_label("Install Application");
    g_signal_connect(button, "clicked", G_CALLBACK(on_button_clicked), "sudo apt-get install vlc");
    gtk_box_pack_start(GTK_BOX(hbox), button, FALSE, FALSE, 0);

    gtk_widget_show_all(window);
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    init_ssh();
    create_gui();

    gtk_main();

    close_ssh();

    return 0;
}
```

This program uses the GTK+ library for the GUI and the libssh library for SSH communication.

To compile and run the program, you need to have the GTK+ and libssh development packages installed. On Ubuntu or Debian, you can install them using:

```
sudo apt-install libgtk-3-dev libssh-dev
```

Then, compile the program with:

```
gcc -o remote_access remote_access.c `pkg-config --cflags --libs gtk+-3.0` -lssh
```

Run the program with:

```
./remote_access
```

Note that you need to replace `username`, `password`, and `target_host` with the appropriate values for your SSH connection.

This program creates a GUI with a text view to display the output of commands and buttons to run commands and install applications on the remote machine. The SSH session is initialized in the `init_ssh()` function and closed in the `close_ssh()` function. The `execute_command()` function is used to execute commands on the remote machine and display the output in the text view.

Keep in mind that this program is a simplified example and may require additional security measures and error handling for a production-ready application. Additionally, the installation of applications on the remote machine requires administrative privileges, and the program does not handle file uploads or downloads.
