from files import generate_pages_recursive, copy_dir

def main():
    copy_dir("static","public")
    generate_pages_recursive(source_path= "content",
                  template_path= "template.html",
                  destination_path= "public")







if __name__ == "__main__":
    main()
