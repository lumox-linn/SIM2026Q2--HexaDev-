import Header from "../../component/head/header";
import "../Home/home.css";
import Testheader from "../../component/testhead/testheaed";
import Footer from "../../component/footer/footer";
import homeimg from "../../assets/homeimg.jpg";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
function Home(props) {
  const location = useLocation();
  const [activeMenu, setActiveMenu] = useState(null);
  const [user, setUser] = useState(null);
  // controll the state of header
  const [isVisible, setIsVisible] = useState(false);
  const closeMenu = () => setActiveMenu(null);
  useEffect(() => {
    const updateUserFromStorage = () => {
      const savedData = localStorage.getItem("userData");
      if (savedData) {
        setUser(JSON.parse(savedData));
      } else {
        setUser(null); // 如果被删了，这里同步设为 null
      }
    };
    updateUserFromStorage();
    window.addEventListener("storage", updateUserFromStorage);
    // get the sessionstorage data
    const lastPage = sessionStorage.getItem("last_page");

    // see if the user come back from none "/home" path
    if (lastPage) {
      // set navigate to visible
      setIsVisible(true);
      // erase this record, incase it will show neext time
      sessionStorage.removeItem("last_external_page");
    }
    return () => window.removeEventListener("storage", updateUserFromStorage);
  }, []);

  return (
    <div className="home">
      <Testheader
        Router={props.Router}
        user={user}
        onNavClick={(idx) => setActiveMenu(idx)}
        isVisible={isVisible}
        setIsVisible={setIsVisible}
      ></Testheader>
      {/* <Header
        Router={props.Router}
        user={user}
        onNavClick={(idx) => setActiveMenu(idx)}
        isVisible={isVisible}
        setIsVisible={setIsVisible}
      ></Header> */}
      <div className="body">
        {/* <img src={homeimg} alt="" className="background" /> */}
        <div id="homecontent">
          _________________________________________________________________________________________________
          SCIT School of Computing and Information Technology Faculty of
          Engineering & Information Sciences SIM Session 2, 2026 Subject Outline
          CSIT314 Software Development Methodologies Subject Organisation
          Subject Coordinator/Lecturer: Dr. Yudi Zhang Email: yudi@uow.edu.au
          Credit Points: 6 credit points Duration: 1 session Lecture Times &
          Location: Refer to SIMConnect The University uses the eLearning system
          Moodle to support all coursework subjects. Students should check the
          subject's Moodle site regularly as important information, including
          details of unavoidable changes in assessment requirements will be
          posted from time to time http://www.uow.edu.au/student/. Any
          information posted to the web site is deemed to have been notified to
          all students. In extraordinary circumstances the provisions stipulated
          in this Subject Outline may require amendment after the Subject
          Outline has been distributed. All students enrolled in the subject
          must be notified and have the opportunity to provide feedback in
          relation to the proposed amendment, prior to the amendment being
          finalised. Data on student performance and engagement (such as Moodle
          and University Library usage, task marks, use of SOLS) will be
          available to the Subject Coordinator to assist in analysing student
          engagement, and to identify and recommend support to students who may
          be at risk of failure. If you have questions about the kinds of data
          the University uses, how we collect it, and how we protect your
          privacy in the use of this data, please refer to
          http://www.uow.edu.au/dvca/bala/analytics/index.html School of
          Computing and Information Technology University of Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 2 of 9 Copyright SCIT, University of Wollongong,
          2026 Subject Description The subject introduces to students modern
          methodologies for software development. Topics may include software
          development life cycle activities, the role of software process
          models, different types of evolutionary models, Unified Process and
          UML, agile principles of software development, Dynamic Systems
          Development Method (DSDM), Scrum and extreme programming, test driven
          software development, the Capability Maturity Model Integration
          (CMMI), software engineering knowledge management, software
          architecture, and emerging trends in software development processes.
          Subject Learning Outcomes On successful completion of this subject,
          students will be able to: 1. Demonstrate an in-depth understanding of
          the stages involved in software development and the issues to be
          considered at each stage 2. Compare and contrast different software
          development methodologies and process models, and assess their
          suitability in different development contexts. 3. Deploy appropriate
          theory, practices, and tools for the specification, design,
          implementation and evaluation of computer-based systems 4. Function
          effectively as part of a team to apply stat-of-the-art software
          development methodologies to the development of a software system 5.
          Apply different strategies for assessing and improving software
          development processes 6. Apply professional standards in software
          development Recent Improvements The School is committed to continual
          improvement in teaching and learning and takes into consideration
          student feedback from many sources. These sources include direct
          student feedback to tutors and lecturers, feedback through Student
          Services and the Faculty Central, and responses to the Subject
          Evaluation Surveys. This information is also used to inform
          comprehensive reviews of subjects and courses. Summary of changes: •
          Remove the overlappings with CSIT214 and CSCI114. • Add new topics
          which reflect current and emerging software development best practices
          in the industry: Principles and practices of continuous integration
          and delivery, DevOps software development practices, Kanban software
          development method, Data-driven software development method, and
          Ethics in developing emerging software systems. Attendance
          Requirements It is the responsibility of students to attend all
          lectures/tutorials/labs/seminars/practical work for subjects for which
          you are enrolled. Satisfactory attendance is deemed by the University,
          to be attendance at approximately 80% of the allocated contact hours.
          School of Computing and Information Technology University of
          Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 3 of 9 Copyright SCIT, University of Wollongong,
          2026 Using Generative Artificial Intelligence (GenAI) GenAI technology
          (such as ChatGPT or Microsoft Co-pilot) is reshaping the University
          experience worldwide. UOW is committed to embracing GenAI as a tool to
          enhance learning experiences and develop vital work-readiness skills.
          However, misuse or use of GenAI in assessments where prohibited
          constitutes academic misconduct (as specified by University Policy).
          It is important that students check if GenAI is permitted for each
          assessment task and how it is to be used and acknowledged. Please read
          the student guidance available on how to use GenAI ethically and
          critically, equally recognising its capabilities and limitations. For
          example: 1. Generative AI is not a substitute for decision-making:
          GenAI should complement, not replace, your critical thinking and
          decision-making skills. 2. Output quality depends on prompts: The
          quality of GenAI outputs is influenced by prompting. Poorly
          constructed or unclear prompts may generate outputs that are
          incorrect. 3. Fact verification is essential: GenAI outputs can be
          fabricated, presenting inaccurate information or contain harmful bias.
          Verify all GenAI outputs against reliable sources. 4. Protect data and
          copyright: Many GenAI technologies collect information in ways that
          breach privacy and data protection provisions, particularly where the
          source material is confidential or subject to copyright. Please check
          the Terms and Conditions of GenAI technologies and if unsure, contact
          UOW Copyright Guidance. 5. Transparency in use: Where required, you
          must acknowledge GenAI use, including providing prompt histories and
          detailing how GenAI was utilised. 6. Thoughtful and appropriate
          application: Be mindful of when and how to use GenAI tools. Assess its
          appropriateness for each use, and refrain from use when not suitable.
          If you have any questions, please contact your Subject Coordinator.
          Method of Presentation The subject will be presented as a series of
          lectures and tutorials. Students must be aware that they are
          responsible for their own learning. Students must prepare adequately
          for lectures and tutorials in order to properly digest the material
          presented in those forms. Students are expected to undertake private
          study in order to fully understand and integrate all the material
          covered in this unit. Lecture Schedule Topics Subject Introduction and
          Software Development Lifecycle Overview of software development
          process models Advanced Unified Modelling Language (UML) School of
          Computing and Information Technology University of Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 4 of 9 Copyright SCIT, University of Wollongong,
          2026 Test-driven development Principles and practices of continuous
          integration and delivery DevOps software development practices Unified
          Software Development Process Extreme programming Kanban software
          development method Capability Maturity Model Integration (CMMI) model
          Data-driven software development Ethics in developing emerging
          software systems Subject Material Any readings/references are
          recommended only and are not intended to be an exhaustive list.
          Students are encouraged to use the library catalogue and databases to
          locate additional readings. Reference Books Roger S. Pressman,
          Software Engineering: A Practitioner's Approach (8th Edition),
          McGraw-Hill Education, 2014 Paul Vii, Scrum: A Cleverly Concise and
          Agile Guide (agile project management, agile product management, agile
          software development, agile development, agile scrum), CreateSpace
          Independent Publishing Platform, 2016 Assessment This subject has the
          following assessment components. ASSESSMENT ITEMS & FORMAT % OF FINAL
          MARK GROUP/ INDIVIDUAL DUE DATE SUBJECT LEARNING OUTCOMES CRITERIA TO
          ASSESS ITEM Lab exercises 10% Individual 1, 2, 3, 5 Correctness,
          completeness, and consistency the School of Computing and Information
          Technology University of Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 5 of 9 Copyright SCIT, University of Wollongong,
          2026 solutions provided by the students with respect to the exercises'
          specification. Project 40% Group 1, 2, 3, 4, 5, 6 Correctness,
          completeness, and consistency the solutions provided by the students
          with respect to the project's specification. Final Examination 50%
          Individual During exam period 1, 2, 3, 5, 6 Correctness, completeness,
          and consistency of the answers provided by the students with respect
          to the exam questions. Notes on Assessment All assignments are
          expected to be completed independently. Plagiarism may result in a
          FAIL grade being recorded for that assignment. Method of Submission of
          Assessment Items Lab exercises and project deliverables are to be
          submitted via Moodle. Arrangement for acknowledging submission of
          written work Electronic acknowledgement by Moodle for submissions.
          Procedure for the return of assessment items The marks of all
          assignments will be returned within 3 weeks of their submission.
          Enquiries regarding the marks should be made within 2 weeks of the
          assignment marks being released. Procedure for the retention of
          assessed work The University may retain copies of student work in
          order to facilitate quality assurance of assessment processes, in
          support of the continuous improvement of assessment design, assessment
          marking and for the review of the subject. The University retains
          records of students’ academic work in accordance with the University
          Records Management Policy and the State Records Act 1988 and uses
          these records in accordance with the University Privacy Policy and the
          Privacy and Personal Information Protection Act 1998. Assessment
          General School of Computing and Information Technology University of
          Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 6 of 9 Copyright SCIT, University of Wollongong,
          2026 Submission of assessment items via email will not be accepted.
          Student contributions to tutorial and/or seminars Not applicable.
          Assessment task is set up to be checked by Turnitin This subject does
          not use Turnitin. Assessment Quality Cycle The University of
          Wollongong is committed to the quality assurance and quality
          enhancement of assessment. The University will meet its legislative
          and regulatory obligations, to ensure consistent and appropriate
          assessment through course management and coordination, including
          assessment quality assurance procedures. An Assessment Quality Cycle
          is used to describe quality assurance at the points of assessment
          design, assessment delivery, the declaration of marks and grades, and
          review and improvement activities. Referencing System The type of
          referencing system to be used for written work is as follows: • the
          Author-Date (Harvard) referencing system is the University’s default
          referencing system to be used in the absence of a documented
          faculty/school preferred referencing style. Refer to the Library
          Referencing and Citing link:
          https://www.uow.edu.au/student/learningcoop/referencingciting/index.html
          Internet Resources There are no restrictions on using Internet
          resources. Technical Fail To be eligible for a Pass in this subject a
          student must achieve a mark of at least 40% in the Final Examination.
          Students who fail to achieve this minimum mark & would have otherwise
          passed may be given a TF (Technical Fail) for this subject. Penalties
          for late submission of assessment items Penalties apply to all late
          work, except if student academic consideration has been granted. Late
          submissions will attract a penalty of 5% of the assessment mark. This
          amount is per day including public holidays and weekends. Work more
          than 4 days late will be awarded a mark of zero. UOW Grade Descriptors
          GRADE DESCRIPTOR School of Computing and Information Technology
          University of Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 7 of 9 Copyright SCIT, University of Wollongong,
          2026 High Distinction(HD) 85-100% For performance that provides
          evidence of an outstanding level of attainment of the relevant subject
          learning outcomes, demonstrating the attributes of a distinction grade
          plus (as applicable) one or more of the following: • consistent
          evidence of deep and critical understanding • substantial originality
          and insight in identifying, generating and communicating competing
          arguments, perspectives or problem-solving approaches • critical
          evaluation of problems, their solutions and their implications • use
          of quantitative analysis of data as the basis for deep and thoughtful
          judgments, drawing insightful, carefully qualified conclusions from
          this work • creativity in application as appropriate to the discipline
          • eloquent and sophisticated communication of information and ideas in
          terms of the conventions of the discipline • consistent application of
          appropriate skills, techniques and methods with outstanding levels of
          precision and accuracy • all or almost all answers correct, very few
          or none incorrect Distinction (D) 75-84% For performance that provides
          evidence of a superior level of attainment of the relevant subject
          learning outcomes, demonstrating the attributes of a credit grade plus
          (as applicable) one or more of the following: • evidence of
          integration and evaluation of critical ideas, principles, concepts
          and/or theories • distinctive insight and ability in applying relevant
          skills, techniques, methods and/or concepts • demonstration of
          frequent originality in defining and analysing issues or problems and
          providing solutions • fluent and thorough communication of information
          and ideas in terms of the conventions of the discipline • frequent
          application of appropriate skills, techniques and methods with
          superior levels of precision and accuracy • most answers correct, few
          incorrect Credit (C) 65-74% For performance that provides evidence of
          a high level of attainment of the relevant subject learning outcomes,
          demonstrating the attributes of a pass grade plus (as applicable) one
          or more of the following: • evidence of learning that goes beyond
          replication of content knowledge or skills • demonstration of solid
          understanding of fundamental concepts in the field of study •
          demonstration of the ability to apply these concepts in a variety of
          contexts • use of convincing arguments with appropriate coherent and
          logical reasoning School of Computing and Information Technology
          University of Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 8 of 9 Copyright SCIT, University of Wollongong,
          2026 • clear communication of information and ideas in terms of the
          conventions of the discipline • regular application of appropriate
          skills, techniques and methods with high levels of precision and
          accuracy • many answers correct, some incorrect Pass (P) 50-64% For
          performance that provides evidence of a satisfactory level attainment
          of the relevant subject learning outcomes, demonstrating (as
          applicable) one or more of the following: • knowledge, understanding
          and application of fundamental concepts of the field of study • use of
          routine arguments with acceptable reasoning • adequate communication
          of information and ideas in terms of the conventions of the discipline
          • ability to apply appropriate skills, techniques and methods with
          satisfactory levels of precision and accuracy • a combination of
          correct and incorrect answers Fail (F) 50% For performance that does
          not provide sufficient evidence of attainment of the relevant subject
          learning outcomes. Technical Fail (TF) When minimum performance level
          requirements for at least one assessment item in the subject as a
          whole has not been met despite the student achieving at least a
          satisfactory level of attainment of the subject learning outcomes.
          https://www.uow.edu.au/curriculum-transformation/aqc/uowgradedescriptors/index.html
          Plagiarism - University’s Academic Integrity Policy The University’s
          policy on acknowledgement practice and plagiarism provides detailed
          information about how to acknowledge the work of others:
          http://www.uow.edu.au/about/policy/UOW058648.html The University’s
          Academic Integrity Policy, Faculty Handbooks and subject guides
          clearly set out the University’s expectation that students submit only
          their own original work for assessment and avoid plagiarising the work
          of others or cheating. Re-using any of your own work (either in part
          or in full) which you have submitted previously for assessment is not
          permitted without appropriate acknowledgement or without the explicit
          permission of the Subject Coordinator. Plagiarism can be detected and
          has led to students being expelled from the University. The use by
          students of any website that provides access to essays or other
          assessment items (sometimes marketed as ‘resources’), is extremely
          unwise. Students who provide an assessment item (or provide access to
          an assessment item) to others, either directly or indirectly (for
          example by uploading an assessment item to a website) are considered
          by the University to be intentionally or recklessly helping other
          students to cheat. Uploading an assessment task, subject outline or
          other course materials without express permission of the university is
          considered academic misconduct and students place themselves at risk
          of being expelled from the University. When you submit an assessment
          task, you are declaring the following School of Computing and
          Information Technology University of Wollongong
          ____________________________________________________________________________________________________
          SIM-2026-S2, Subject Outline, CSIT314: Software Development
          Methodologies Page 9 of 9 Copyright SCIT, University of Wollongong,
          2026 1. It is your own work and you did not collaborate with or copy
          from others. 2. You have read and understand your responsibilities
          under the University of Wollongong's Academic Integrity Policy on
          plagiarism. 3. You have not plagiarised from published work (including
          the internet). Where you have used the work from others, you have
          referenced it in the text and provided a reference list at the end to
          the assignment. Students must remember that: • Plagiarism will not be
          tolerated. • Students are responsible for submitting original work for
          assessment, without plagiarising or cheating, abiding by the
          University’s Academic Integrity Policy as set out in the University
          Handbook, the University's online Policy Directory and in Faculty
          handbooks and subject guides. Student Academic Complaints Policy
          (Coursework or Higher Degree Research) In accordance with the
          Coursework Student Academic Complaints Policy, a student may request
          an explanation of a mark for an assessment task or a final grade for a
          subject consistent with the student’s right to appropriate and useful
          feedback on their performance in an assessment task. Refer to the
          Coursework Student Academic Complaints Policy for further information
          http://www.uow.edu.au/about/policy/UOW058653.html General Advice This
          outline should be considered in conjunction with policy documents
          available through the University of Wollongong website. Those policies
          are subject to revision.
        </div>
        <Footer></Footer>
      </div>

      {activeMenu !== null && (
        <div className="mask">
          <div className="big-box" onClick={(e) => e.stopPropagation()}>
            <i className="x" onClick={closeMenu}>
              X
            </i>
            <div className="searchbar">
              <input type="text" placeholder="Search" className="search" />

              <button
                className="searbutton"
                onClick={(e) => {
                  console.log(e);
                }}
              >
                Search
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default Home;
