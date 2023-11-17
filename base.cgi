#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);

# Retrieve form inputs
my $first_name   = param('firstName');
my $last_name    = param('lastName');
my $street       = param('street');
my $city         = param('city');
my $postal_code  = param('postalCode');
my $province     = param('province');
my $phone        = param('phone');
my $email        = param('email');

# Validate inputs
my $phone_error        = check_phone($phone);
my $postal_code_error  = check_postal_code($postal_code);
my $email_error        = check_email($email);

# Print HTML header
print header;

# Print HTML content
print <<"HTML";
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Results</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f8f8;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            color: #333;
        }

        .result-box {
            width: 80%;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h2 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
            font-size: 24px;
        }

        /* Add styles for different sections */
        .result-section {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
        }

        .personal-section {
            background-color: #ecf0f1;
        }

        .address-section {
            background-color: #9acfe6;
        }

        .contact-section {
            background-color: #fdebd0;
        }

        .result-box div {
            margin-bottom: 20px;
        }

        .error {
            color: #e74c3c;
            font-weight: bold;
        }

        .photo {
            width: 100%;
            max-width: 100%;
            height: auto;
            margin-top: 20px;
            border-radius: 8px;
        }

        .tag {
            color: #1c42b5;
            font-weight: bold;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="result-box">
        <h2>Registration Results</h2>
HTML

# Display results for personal information
display_result("Personal Information", "First Name", $first_name);
display_result("", "Last Name", $last_name);


display_result("Address Information", "Street Name", $street);
display_result("", "City", $city);
display_result("", "Province", $province);
display_result("", "Postal Code", $postal_code, $postal_code_error);


display_result("Contact Information", "Phone Number", $phone, $phone_error);
display_result("", "Email Address", $email, $email_error);


my $uploaded_file = upload('photo');
if ($uploaded_file) {
    my $filename = "../lab07/Images/$first_name$last_name.jpg";  # Replace with the actual directory path
    open my $fh, '>', $filename or die "Cannot open file: $!";
    binmode $fh;
    while (my $chunk = <$uploaded_file>) {
        print $fh $chunk;
    }
    close $fh;
    print qq(<img src="../lab07/Images/$first_name$last_name.jpg" alt="photo" class="photo" />);  # Adjust the path accordingly
}


print <<"HTML";
    </div>
</body>
</html>
HTML

sub display_result {
    my ($section, $tag, $value, $error) = @_;
    print "<div class='result-section $section'>";
    print "<h3>$section</h3>" if $section;
    print "<p class='tag'>$tag:</p>";
    if ($error) {
        print "<p class='error'>$error</p>";
    } else {
        print "<p>$value</p>";
    }
    print "</div>";
}


sub check_phone {
    my $phone = shift;
    return "Invalid phone number (Enter only 10 digits)" unless $phone =~ /^\d{10}$/;
    return;
}


sub check_postal_code {
    my $postal_code = shift;
    return "Invalid postal code format (L0L 0L0)" unless $postal_code =~ /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/;
    return;
}


sub check_email {
    my $email = shift;
    return "Invalid email address" unless $email =~ /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return;
}
