# Task 3: NLP Preprocessing and Method Selection

## Objective

Clean, structure and preprocess job-posting text for NLP. Methods and libraries are each member's
own choice, but the output quality bar is shared so cross-company comparison stays fair.

## What is submitted

**Each member (in their own folder)**

1. Cleaned and preprocessed job-posting text
2. The documented preprocessing workflow, with code committed to this repository

## Rules for this task

- Everyone produces a `cleaned_description` column. Same name, same position in the schema, so the
  Task 6 joins work without per-member special cases.
- Do not drop rows silently. Log what was removed and why; rows in and rows out both get reported.
- Notebooks and scripts must run top to bottom from a clean checkout.
- State the library versions used in your note.

## Definition of done

- [ ] Cleaned dataset committed
- [ ] Preprocessing note committed, covering method choice, pipeline steps and limitations
- [ ] Code committed and re-runnable
- [ ] Rows in / rows out reconciled
- [ ] A sample validated by hand, with anything it caught written up

## Status

| Member | Company | Submitted | Reviewed by |
|---|---|---|---|
| Nayab Khalid | NVIDIA | [x] | |
| Noorul Huda Batool | Google | [ ] | |
| Arham Malik | Microsoft | [ ] | |
| Abdal Farid | Meta | [ ] | |

## Open team decisions raised by this task

1. **The seniority vocabulary needs extending.** `docs/data-schema.md` lists Junior, Mid, Senior,
   Lead and Principal. NVIDIA titles also carry Intern, Staff, Distinguished, Director and
   Executive. The extended set is in use and flagged rather than forcing real values into five
   buckets. Needs ratifying so all four members use one list.
2. **`cleaned_description` means different things per member.** For members with description text it
   is preprocessed prose; for NVIDIA it is a preprocessed title. Anything comparing text length,
   vocabulary size or token counts across companies must account for this or it compares nothing.

See [Nayab's preprocessing note](nvidia-nayab-khalid/preprocessing-note.md), sections 2 and 8.

Due date: to be agreed in the sprint meeting.
Portal submission: the URL of this repository.
