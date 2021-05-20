#include <stdio.h>
#include <stdlib.h>

// ---- Objects ----
typedef struct Lecture{
    char* code; // Ders kodu
    char* name; // Adi
    int credit, quota; // toplam kredisi, kontenjani
    char* lecturer_id; // ogr. uyesinin ID numarasi
} Lecture;

typedef struct Lecturer{
    char* id; // ID numarasi
    char* f_name; // Adi
    char* l_name; // Soyadi
    char* title; // Unvani
} Lecturer;

typedef struct Student{
    char* id; // ogrenci numarasi
    char* f_name; // Adi  
    char* l_name; // Soyadi
    int total_lectures, total_credit; // toplam ders sayisi, toplam kredi
    int max_lectures, max_credit; // maximum degerleri
} Student;


// ---- Object Utilities ----
// -- Lecture --
Lecture* getLecture(){ // constructor
    Lecture *lctr = (Lecture*) malloc(sizeof(Lecture));
    if (lctr == NULL){
        printf("Lecture olusulamadi.");
        exit(1);
    }
    int credit, quota;
    char *code, *name, *lecturer_id;
    printf("Ders Kodu: "); scanf("%s", code);
    printf("\nDers Adi: "); scanf("%s", name);
    printf("\nKredisi: "); scanf("%d", credit);
    printf("\nKontenjani: "); scanf("%d", quota);
    printf("\nDersi veren Ogr. Uyesinin ID'si: "); scanf("%s", lecturer_id);
    printf("\n");

    lctr->code = strdup(code);
    lctr->name = strdup(name);
    lctr->lecturer_id = strdup(lecturer_id);
    lctr->credit = credit;
    lctr->quota = quota;
    
    return lctr;
}

void addLecture(FILE* fin, Lecture* lectr){ // Ders ekleme islemi
    
    fprintf(fin, "%s, %s, %d, %d, %s",
            lectr->code, lectr->name,
            lectr->credit, lectr->quota,
            lectr->lecturer_id);
    
}


// -- Lecturer --
Lecturer* getLecturer(){ // constructor
    Lecturer *lctrr = (Lecturer*) malloc(sizeof(Lecturer));
    if (lctrr == NULL){
        printf("Lecturer olusulamadi.");
        exit(1);
    }
    
    printf("ID: "); scanf("%s", lctrr->id);
    printf("\nAdi: "); scanf("%s", lctrr->f_name);
    printf("\nSoyadi: "); scanf("%s", lctrr->l_name);
    printf("\nUnvani: "); scanf("%s", lctrr->title);
    printf("\n");

    printf("Returned !!!!!!!");
    return lctrr;
}

void addLecturer(FILE* fin, Lecturer* lectrr){
    
    fprintf(fin, "%s, %s, %s, %s",
            lectrr->id,
            lectrr->f_name, lectrr->l_name,
            lectrr->title);
    
}

// -- Student --
Student* getStudent(){ // constructor
    Student *stdnt = (Student*) malloc(sizeof(Student));
    if (stdnt == NULL){
        printf("Student olusulamadi.");
        exit(1);
    }
    
    printf("Ogrenci numarasi: "); scanf("%s", stdnt->id);
    printf("\nAdi: "); scanf("%s", stdnt->f_name);
    printf("\nSoyadi: "); scanf("%s", stdnt->l_name);
    printf("\nMaximum Ders Sayisi: "); scanf("%d", &stdnt->max_lectures);
    printf("\nMaximum Kredi: "); scanf("%d", &stdnt->max_credit);
    printf("\n");

    stdnt->total_credit = 0;
    stdnt->total_lectures = 0;

    return stdnt;
}

void add_Student(FILE* fin, Student* std){
    
    fprintf(fin, "%s, %s, %s, %d, %d",
            std->id,
            std->f_name, std->l_name,
            std->total_credit , std->total_lectures);
        
}
// ---- File Utilities ----


// ---- Menu ----
void printMainMenu(){
    printf ("\n--------------------------------\n");
    printf ("--- Ana Menu ---\n"
            "\t1. Dersler\n"
            "\t2. Ogretim Uyeleri\n"
            "\t3. Ogrenciler\n"
            "\t0. Cikis\n");
}
void printLectureMenu(){
    printf ("---------------\n");
    printf ("--- Dersler ---\n"
            "\t1. Yeni Ders Ekle\n"
            "\t2. Dersi Sil\n"
            "\t3. Dersi Guncelle\n");
}
void printLecturerMenu(){
    printf ("---------------\n");
    printf ("--- Ogretim Uyeleri ---\n"
            "\t1. Yeni Ogr. Uyesi Ekle\n"
            "\t2. Ogr. Usesini Sil\n"
            "\t3. Ogr. Uyesini Guncelle\n");
}
void printStudentMenu(){
    printf ("---------------\n");
    printf ("--- Ogrenci ---\n"
            "\t1. Yeni Ogrenci Ekle\n"
            "\t2. Ogrenciyi Sil\n"
            "\t3. Ogrenciyi Guncelle\n");
}


// ---- Main ----
int main(){
    Lecture* lectr;
    Lecturer* lectrr;
    Student* stdnt;

    FILE *f_lectures = fopen("./Dersler.txt", "r+");
    FILE *f_lecturers = fopen("./OgretimUyeleri.txt", "r+");
    FILE *f_students = fopen("./Ogrenciler.txt", "r+");
    
    char opt, subopt;
    char* input; // switch icinde girilir.

    while (opt != '0'){
        // Main Menu
        printMainMenu();
        opt = getchar();
        getchar(); // Junk

        if(opt == '1'){ // Lecture Menu
            printLectureMenu();
            subopt = getchar();

            if(subopt == '1'){ // Add Lecture to file
                lectr = getLecture();
                printf("Olustu, mesela %d", lectr->quota);
                addLecture(f_lectures, lectr);
            }
            else if(subopt == '2'){
                printf("ID giriniz: ");
                scanf("%s", input);
                //removeLecture(f_lectures, id);
            }
            else if(subopt == '3'){
                printf("ID giriniz: ");
                scanf("%s", input);
                printf("Yeni dersi giriniz");
                lectr = getLecture();
                //updateLecture(f_lectures, input, lectr);
            }
            else
                printf("Lutfen uygun olarak giris yapiniz.\n");
        }
        else if(opt == '2'){ // Lecturer Menu
            printLecturerMenu();
            subopt = getchar();

            if(subopt == '1'){// Add Lecturer to file
                lectrr = getLecturer();
                addLecturer(f_lecturers, lectrr);
            }
            else if(subopt == '2'){
                printf("ID giriniz: ");
                scanf("%s", input);
                //removeLecturer(f_lecturers, id);
            }
            else if(subopt == '3'){
                printf("ID giriniz: ");
                scanf("%s", input);
                printf("Yenilikleri giriniz");
                lectrr = getLecturer();
                //updateLecture(f_lectures, input, lectrr);
            }
            else
                printf("Lutfen uygun olarak giris yapiniz.\n");
        }
        else if(opt == '3'){ // Student Menu
            printStudentMenu();
            subopt = getchar();

            if(subopt=='1'){// Add Student to file
                stdnt = getStudent();
                add_Student(f_students, stdnt);
            }
            if(subopt == '2'){
                printf("Ogrenci numarasini giriniz: ");
                scanf("%s", input);
                //removeLecture(f_lectures, id);
            }
            if(subopt == '3'){
                printf("Ogrenci numarasini  giriniz: ");
                scanf("%s", input);
                printf("Yenilikleri giriniz");
                stdnt = getStudent();
                //updateLecture(f_lectures, input, lectr);
            }
            else
                printf("Lutfen uygun olarak giris yapiniz.\n");
            
        }
        else{
            printf("Lutfen uygun olarak giris yapiniz.\n");
        }
        
    }

    printf("Program bitti!");

    free(lectr);
    free(lectrr);
    free(stdnt);

    fclose(f_lectures);
    fclose(f_lecturers);
    fclose(f_students);

    return 0;
}