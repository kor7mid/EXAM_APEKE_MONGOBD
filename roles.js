// Création du rôle pour les étudiants
db.createRole({
  role: 'student_role',
  privileges: [
    {
      resource: { db: 'university', collection: 'students' },
      actions: ['find', 'insert', 'update', 'remove'],
    },
  ],
  roles: [],
});

// Création du rôle pour les enseignants
db.createRole({
  role: 'teacher_role',
  privileges: [
    {
      resource: { db: 'university', collection: 'teachers' },
      actions: ['find', 'insert', 'update', 'remove'],
    },
  ],
  roles: [],
});

// Création du rôle pour le personnel administratif
db.createRole({
  role: 'admin_staff_role',
  privileges: [
    {
      resource: { db: 'university', collection: 'admin_staff' },
      actions: ['find', 'insert', 'update', 'remove'],
    },
  ],
  roles: [],
});

// Création du rôle pour les sports
db.createRole({
  role: 'sports_role',
  privileges: [
    {
      resource: { db: 'university', collection: 'sports' },
      actions: ['find', 'insert', 'update', 'remove'],
    },
  ],
  roles: [],
});

// Création de l'utilisateur pour les étudiants
db.createUser({
  user: 'student_user',
  pwd: 'password',
  roles: ['student_role'],
});

// Création de l'utilisateur pour les enseignants
db.createUser({
  user: 'teacher_user',
  pwd: 'password',
  roles: ['teacher_role'],
});

// Création de l'utilisateur pour le personnel administratif
db.createUser({
  user: 'admin_staff_user',
  pwd: 'password',
  roles: ['admin_staff_role'],
});

// Création de l'utilisateur pour les sports
db.createUser({
  user: 'sports_user',
  pwd: 'password',
  roles: ['sports_role'],
});
